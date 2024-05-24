import logging
import os
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path
from typing import Dict, Iterator, List, Mapping, Optional, Set, TextIO, Tuple, Union, cast
from urllib.parse import urlparse

from jsonasobj2 import values
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    ClassDefinitionName,
    ElementName,
    EnumDefinition,
    EnumDefinitionName,
    SchemaDefinition,
    SlotDefinition,
    SlotDefinitionName,
    TypeDefinition,
    TypeDefinitionName,
)
from linkml_runtime.utils.context_utils import parse_import_map
from linkml_runtime.utils.formatutils import camelcase, mangled_attribute_name, sfx, underscore
from linkml_runtime.utils.metamodelcore import Bool
from linkml_runtime.utils.namespaces import Namespaces
from linkml_runtime.utils.yamlutils import TypedNode

from linkml.utils.mergeutils import merge_classes, merge_schemas, merge_slots, slot_usage_name
from linkml.utils.rawloader import load_raw_schema
from linkml.utils.schemasynopsis import SchemaSynopsis


class SchemaLoader:
    def __init__(
        self,
        data: Union[str, TextIO, SchemaDefinition, dict, Path],
        base_dir: Optional[str] = None,
        namespaces: Optional[Namespaces] = None,
        useuris: Optional[bool] = None,
        importmap: Optional[Mapping[str, str]] = None,
        logger: Optional[logging.Logger] = None,
        mergeimports: Optional[bool] = True,
        emit_metadata: Optional[bool] = True,
        source_file_date: Optional[str] = None,
        source_file_size: Optional[int] = None,
    ) -> None:
        """Constructor - load and process a YAML or pre-processed schema

        :param data: YAML schema text, python dict loaded from yaml,  URL, file name, open file or SchemaDefinition
        :param base_dir: base directory or URL where Schema came from
        :param namespaces: namespaces collector
        :param useuris: True means class_uri and slot_uri are identifiers.  False means they are mappings.
        :param importmap: A map from import entries to URI or file name.
        :param logger: Target Logger, if any
        :param mergeimports: True means combine imports into single package. False means separate packages
        :param emit_metadata: True means include source file, size and date
        :param source_file_date: modification of source file
        :param source_file_size: size of source file
        """
        self.logger = logger if logger is not None else logging.getLogger(self.__class__.__name__)
        if isinstance(data, SchemaDefinition):
            self.schema = data
        else:
            self.schema = load_raw_schema(
                data,
                base_dir=base_dir,
                merge_modules=mergeimports,
                source_file_date=source_file_date,
                source_file_size=source_file_size,
            )
        # Map from URI to source and version tuple
        self.loaded: OrderedDict[str, Tuple[str, str]] = {
            self.schema.id: (self.schema.source_file, self.schema.version)
        }
        self.base_dir = self._get_base_dir(base_dir)
        self.namespaces = namespaces if namespaces else Namespaces()
        self.useuris = useuris if useuris is not None else True
        self.importmap = parse_import_map(importmap, self.base_dir) if importmap is not None else dict()
        self.source_file_date = source_file_date
        self.source_file_size = source_file_size
        self.synopsis: Optional[SchemaSynopsis] = None
        self.schema_location: Optional[str] = None
        self.schema_defaults: Dict[str, str] = {}  # Map from schema URI to default namespace
        self.merge_modules = mergeimports
        self.emit_metadata = emit_metadata

    def resolve(self) -> SchemaDefinition:
        """Reconcile a loaded schema, applying is_a, mixins, apply_to's and other such things.  Also validate the
        content and load a SchemaSynopsis entry

        :return: Fully resolved definition
        """
        if not self.schema.default_range:
            self.schema.default_range = "string"
            self.logger.info(f"Default_range not specified. Default set to '{self.schema.default_range}'")

        # Process the namespace declarations
        if not self.schema.default_prefix:
            self.schema.default_prefix = sfx(self.schema.id)
        self.schema_defaults[self.schema.id] = self.schema.default_prefix
        for prefix in self.schema.prefixes.values():
            self.namespaces[prefix.prefix_prefix] = prefix.prefix_reference
        for cmap in self.schema.default_curi_maps:
            self.namespaces.add_prefixmap(cmap, include_defaults=False)

        # Process imports
        for imp in self.schema.imports:
            sname = self.importmap.get(str(imp), imp)  # Import map may use CURIE
            # substitute CURIE only if we don't have a local file name with drive letter (windows)
            if not os.path.splitdrive(sname)[0]:
                if ":" in sname:
                    # allow mapping of a prefix to a folder/directory
                    toks = sname.split(":")
                    pfx = toks[0]
                    if pfx in self.importmap:
                        sname = os.path.join(self.importmap[pfx], ":".join(toks[1:]))
                    else:
                        sname = self.namespaces.uri_for(sname)
            sname = self.importmap.get(str(sname), sname)  # It may also use URI or other forms
            import_schemadefinition = load_raw_schema(
                sname + ".yaml",
                base_dir=os.path.dirname(self.schema.source_file) if self.schema.source_file else self.base_dir,
                merge_modules=self.merge_modules,
                emit_metadata=self.emit_metadata,
            )
            loaded_schema = (str(sname), import_schemadefinition.version)
            if import_schemadefinition.id in self.loaded:
                # If we've already loaded this, make sure that we've got the same version
                if self.loaded[import_schemadefinition.id][1] != loaded_schema[1]:
                    self.raise_value_error(
                        f"Schema {import_schemadefinition.name} - version mismatch",
                        import_schemadefinition.name,
                    )
                # Note: for debugging purposes we also check whether the version
                #       came from the same spot.  This should be loosened to
                #       version only once we're sure that everything is working
                # TODO: The test below needs review -- there are cases where it
                #       fails because self.loaded[...][0] has the full path name
                #       and loaded_schema[0] is just the local name
                # if self.loaded[import_schemadefinition.id] != loaded_schema:
                #     self.raise_value_error(f"Schema imported from different files: "
                #                            f"{self.loaded[import_schemadefinition.id][0]} : {loaded_schema[0]}")
            else:
                self.loaded[import_schemadefinition.id] = loaded_schema
                merge_schemas(
                    self.schema,
                    import_schemadefinition,
                    imp,
                    self.namespaces,
                    merge_imports=self.merge_modules,
                )
                self.schema_defaults[import_schemadefinition.id] = import_schemadefinition.default_prefix

        if not self.namespaces._default:
            if "://" in self.schema.default_prefix:
                self.namespaces._default = self.schema.default_prefix
            elif self.schema.default_prefix in self.namespaces:
                self.namespaces._default = self.namespaces[self.schema.default_prefix]
            else:
                self.raise_value_error(
                    f"Default prefix: {self.schema.default_prefix} is not defined",
                    self.schema.default_prefix,
                )

        self.namespaces._base = (
            self.schema.default_prefix
            if ":" in self.schema.default_prefix
            else self.namespaces[self.schema.default_prefix]
        )

        # Promote embedded attribute definitions to first class slots.
        for cls in self.schema.classes.values():
            for attribute in cls.attributes.values():
                mangled_slot_name = mangled_attribute_name(cls.name, attribute.name)
                if mangled_slot_name in self.schema.slots:
                    # mangled names are overwritten if a schema with attributes is passed in
                    # TODO: handle this in a more graceful way
                    #  see https://github.com/linkml/linkml/issues/872
                    logging.warning(
                        f'Class: "{cls.name}" attribute "{attribute.name}" - '
                        f"mangled name: {mangled_slot_name} already exists",
                    )
                new_slot = SlotDefinition(**attribute.__dict__)
                new_slot.domain_of.append(cls.name)
                new_slot.imported_from = cls.imported_from
                new_slot.from_schema = cls.from_schema
                if not new_slot.alias:
                    new_slot.alias = attribute.name
                new_slot.name = mangled_slot_name
                self.schema.slots[new_slot.name] = new_slot
                cls.slots.append(mangled_slot_name)

        # Assign class slot ownership
        for cls in self.schema.classes.values():
            if not isinstance(cls, ClassDefinition):
                name = cls["name"] if "name" in cls else "Unknown"
                self.raise_value_error(
                    f'Class "{name} (type: {type(cls)})" definition is not a class definition',
                    name,
                )
            if isinstance(cls.slots, str):
                self.logger.warning(f"File: {self.schema.source_file} Class: {cls.name} Slots are not an array")
                cls.slots = [cls.slots]
            for slotname in cls.slots:
                if slotname in self.schema.slots:
                    slot = self.schema.slots[cast(SlotDefinitionName, slotname)]
                    slot.owner = cls.name
                    if cls.name not in slot.domain_of:
                        slot.domain_of.append(cls.name)
                else:
                    self.raise_value_error(f'Class "{cls.name}" - unknown slot: "{slotname}"', slotname)

        # Process slots defined as slot usages
        self.process_slot_usage_definitions()

        # Massage initial set of slots
        for slot in self.schema.slots.values():
            # Propagate domain to containing class
            if slot.domain and slot.domain in self.schema.classes:
                if slot.name not in self.schema.classes[slot.domain].slots:
                    slot.owner = slot.name
                    # self.schema.classes[slot.domain].slots.append(slot.name)
            elif slot.domain:
                self.raise_value_error(
                    f"slot: {slot.name} - unrecognized domain ({slot.domain})",
                    slot.domain,
                )

            # Validate the slot range
            if (
                slot.range is not None
                and slot.range not in self.schema.types
                and slot.range not in self.schema.classes
                and slot.range not in self.schema.enums
            ):
                self.raise_value_error(f"slot: {slot.name} - unrecognized range ({slot.range})", slot.range)

            # check constraints for usage of equals_string and equals_string_in
            self._check_equals_string(slot)

        # apply to --> mixins
        for cls in self.schema.classes.values():
            for apply_to_cls in cls.apply_to:
                if apply_to_cls in self.schema.classes:
                    self.schema.classes[apply_to_cls].mixins.append(cls.name)
                else:
                    self.raise_value_error(
                        f'Class "{cls.name}" unknown apply_to target: {apply_to_cls}',
                        apply_to_cls,
                    )
            # Class URI's also count as (trivial) mappings
            if cls.class_uri is not None:
                cls.mappings.insert(0, cls.class_uri)
            if cls.class_uri is None or not self.useuris:
                from_schema = cls.from_schema
                if from_schema is None:
                    from_schema = self.schema.id
                # if cls.from_schema is None:
                #    raise Exception(f"Class has no from_schema: {cls}")
                suffixed_cls_schema = sfx(from_schema)
                cls.class_uri = self.namespaces.uri_or_curie_for(
                    self.schema_defaults.get(cls.from_schema, suffixed_cls_schema),
                    camelcase(cls.name),
                )

        # Get the inverse ducks all in a row before we start filling other stuff in
        for slot in self.schema.slots.values():
            if slot.inverse:
                inverse_slot = self.schema.slots.get(slot.inverse, None)
                if inverse_slot:
                    if not inverse_slot.inverse:
                        inverse_slot.inverse = slot.name
                    elif inverse_slot.inverse != slot.name:
                        self.raise_value_error(
                            f"Slot {slot.name}.inverse ({slot.inverse}) does not match "
                            f"slot {inverse_slot.name}.inverse ({inverse_slot.inverse})"
                        )
                else:
                    self.raise_value_error(f"Slot {slot.name}.inverse ({slot.inverse}) is not defined")

        # Update slots with parental information
        merged_slots: List[SlotDefinitionName] = []
        for slot in self.schema.slots.values():
            if not slot.from_schema:
                slot.from_schema = self.schema.id
            self.merge_slot(slot, merged_slots)
            # Add default ranges
            if slot.range is None:
                # Inverses will be handled later on in the process
                if not slot.inverse:
                    slot.range = self.schema.default_range

        # Update enums
        for enum in self.schema.enums.values():
            if not enum.from_schema:
                enum.from_schema = self.schema.id
            # TODO: Need to add "is_a" to enums
            # self.merge_enum(enum, merged_enums)

        # Process the slot_usages
        for cls in self.schema.classes.values():
            self.process_slot_usages(cls)
            if not cls.from_schema:
                cls.from_schema = self.schema.id

        # Merge class with its mixins and the like
        merged_classes: List[ClassDefinitionName] = []
        for cls in self.schema.classes.values():
            self.merge_class(cls, merged_classes)

        # Update types with parental information
        merged_types: List[TypeDefinitionName] = []
        for typ in self.schema.types.values():
            if not typ.base and not typ.typeof:
                self.raise_value_error(
                    f'type "{typ.name}" must declare a type base or parent (typeof)',
                    typ.name,
                )
            if not typ.typeof and not typ.uri:
                self.raise_value_error(f'type "{typ.name}" does not declare a URI', typ.name)
            self.merge_type(typ, merged_types)
            if not typ.from_schema:
                typ.from_schema = self.schema.id

        # Update the subsets as needed
        for ss in self.schema.subsets.values():
            if not ss.from_schema:
                ss.from_schema = self.schema.id

        # Massage initial set of slots
        for slot in self.schema.slots.values():
            # Keys and identifiers must be present
            if bool(slot.key or slot.identifier):
                if slot.required is None:
                    slot.required = True
                elif not slot.required:
                    self.raise_value_error(
                        f"slot: {slot.name} - key and identifier slots cannot be optional",
                        slot.name,
                    )
                if slot.key and slot.identifier:
                    self.raise_value_error(
                        f"slot: {slot.name} - A slot cannot be both a key and identifier at the same time",
                        slot.name,
                    )

            # Propagate domain to containing class
            if slot.domain and slot.domain in self.schema.classes:
                if slot.name not in self.schema.classes[slot.domain].slots and not slot.owner:
                    slot.owner = slot.name
                    # Slot domains to not appear
                    # self.schema.classes[slot.domain].slots.append(slot.name)
            elif slot.domain:
                self.raise_value_error(
                    f"slot: {slot.name} - unrecognized domain ({slot.domain})",
                    slot.domain,
                )

            # Keys and identifiers must be present
            if bool(slot.key or slot.identifier):
                if slot.required is None:
                    slot.required = True
                elif not slot.required:
                    self.raise_value_error(
                        f"slot: {slot.name} - key and identifier slots cannot be optional",
                        slot.name,
                    )

            # Validate the slot range
            if (
                slot.range is not None
                and slot.range not in self.schema.types
                and slot.range not in self.schema.classes
                and slot.range not in self.schema.enums
            ):
                self.raise_value_error(f"slot: {slot.name} - unrecognized range ({slot.range})", slot.range)

            # check constraints for usage of equals_string and equals_string_in
            self._check_equals_string(slot)

        # Massage classes, propagating class slots entries domain back to the target slots
        for cls in self.schema.classes.values():
            if not isinstance(cls, ClassDefinition):
                name = cls["name"] if "name" in cls else "Unknown"
                self.raise_value_error(f'Class "{name} (type: {type(cls)})" definition is not a class definition')
            if isinstance(cls.slots, str):
                self.logger.warning(f"File: {self.schema.source_file} Class: {cls.name} Slots are not an array")
                cls.slots = [cls.slots]
            for slotname in cls.slots:
                if slotname in self.schema.slots:
                    slot = self.schema.slots[cast(SlotDefinitionName, slotname)]
                else:
                    self.raise_value_error(f'Class "{cls.name}" - unknown slot: "{slotname}"', slotname)

        for slot in self.schema.slots.values():
            if slot.from_schema is None:
                slot.from_schema = self.schema.id
            # Inline any class definitions that don't have identifiers.  Note that keys ARE inlined
            if slot.range in self.schema.classes:
                range_class = self.schema.classes[cast(ClassDefinitionName, slot.range)]
                if slot.inlined_as_list or not any(
                    [self.schema.slots[s].identifier or self.schema.slots[s].key for s in range_class.slots]
                ):
                    slot.inlined = True

            if slot.slot_uri is not None:
                slot.mappings.insert(0, slot.slot_uri)
            # Assign missing predicates
            if slot.slot_uri is None or not self.useuris:
                slot.slot_uri = self.namespaces.uri_or_curie_for(
                    self.schema_defaults.get(slot.from_schema, sfx(slot.from_schema)),
                    self.slot_name_for(slot),
                )

            if slot.subproperty_of and slot.subproperty_of not in self.schema.slots:
                self.raise_value_error(
                    f'Slot: "{slot.name}" - subproperty_of: "{slot.subproperty_of}" '
                    f"does not reference a slot definition",
                    slot.subproperty_of,
                )

        # Evaluate any slot inverses
        def domain_range_alignment(fwd_slot: SlotDefinition, inverse_slot: SlotDefinition) -> bool:
            """Determine whether the range of fwd_slot is compatible with the domain of inverse_slot"""
            # TODO: Determine what to do about class and slot hierarchy
            if fwd_slot.range and fwd_slot.range not in self.schema.classes:
                raise ValueError(
                    f"Slot '{fwd_slot.name}' range ({fwd_slot.range}) is not an class -- inverse is not possible"
                )
            if fwd_slot.domain:
                if not inverse_slot.range:
                    inverse_slot.range = fwd_slot.domain
                elif not domain_range_alignment(fwd_slot, inverse_slot):
                    self.logger.warning(f"Slot: {slot.name} and inverse slot: {inverse_slot.name} are not compatible")
            return True

        # Get the inverse domains and ranges sorted
        for slot in self.schema.slots.values():
            if slot.inverse:
                # Note that the inverse OF the inverse will be caught in this same iterator
                inverse_slot = self.schema.slots[slot.inverse]
                if not slot.range:
                    if inverse_slot.domain:
                        slot.range = inverse_slot.domain
                    elif len(inverse_slot.domain_of):
                        if len(inverse_slot.domain_of) > 1:
                            dom_list = ", ".join(inverse_slot.domain_of)
                            self.logger.warning(
                                f"Slot {slot.name}.inverse ({inverse_slot.name}), "
                                f"has multi domains ({dom_list})  Multi ranges not yet implemented"
                            )
                        slot.range = inverse_slot.domain_of[0]
                    else:
                        raise ValueError(
                            f"Unable to determine the range of slot `{slot.name}'. "
                            f"Its inverse ({inverse_slot.name}) has no declared domain"
                        )
                elif not inverse_slot.domain and len(inverse_slot.domain_of) == 0:
                    inverse_slot.domain = slot.range
                elif slot.range not in (inverse_slot.domain, inverse_slot.domain_of):
                    self.logger.warning(
                        f"Range of slot '{slot.name}' ({slot.range}) "
                        f"does not line with the domain of its inverse ({inverse_slot.name})"
                    )

        # Check for duplicate class and type names
        def check_dups(s1: Set[ElementName], s2: Set[ElementName]) -> Tuple[List[ElementName], str]:
            if s1.isdisjoint(s2):
                return [], ""

            # Return an ordered list of d1/d1 tuples
            # For some curious reason, s1.intersection(s2) and s2.intersection(s1) BOTH yield s1 elements
            dups = sorted(s1.intersection(s2))
            dup_locs = list()
            for dup in dups:
                dup_locs += [s1e for s1e in s1 if s1e == dup]
                dup_locs += [s2e for s2e in s2 if s2e == dup]

            return dup_locs, ", ".join(dups)

        classes = set(self.schema.classes.keys())
        self.validate_item_names("class", classes)
        slots = set(self.schema.slots.keys())
        self.validate_item_names("slot", slots)
        types = set(self.schema.types.keys())
        self.validate_item_names("type", types)
        subsets = set(self.schema.subsets.keys())
        self.validate_item_names("subset", subsets)
        enums = set(self.schema.enums.keys())
        self.validate_item_names("enum", enums)

        # Check that the default range is valid
        default_range_needed = any(slot.range == self.schema.default_range for slot in self.schema.slots.values())
        if (
            default_range_needed
            and self.schema.default_range not in self.schema.types
            and self.schema.default_range not in self.schema.classes
        ):
            raise ValueError(f'Unknown default range: "{self.schema.default_range}"')

        # We are currently limited to one key per class
        for cls in self.schema.classes.values():
            class_slots = []
            for sn in cls.slots:
                slot = self.schema.slots[sn]
                if slot.key or slot.identifier:
                    class_slots.append(sn)
            if len(class_slots) > 1:
                self.raise_value_error(
                    f'Class "{cls.name}" - multiple keys/identifiers not allowed ({", ".join(class_slots)})',
                    class_slots[1],
                )

        # Check out all the namespaces
        self.check_prefixes()

        # Cannot have duplicate class or type keys
        dups, items = check_dups(types, classes)
        if items:
            self.raise_value_errors(f"Overlapping type and class names: {items}", dups)
        dups, items = check_dups(enums, classes)
        if items:
            self.raise_value_errors(f"Overlapping enum and class names: {items}", dups)
        dups, items = check_dups(types, enums)
        if items:
            self.raise_value_errors(f"Overlapping type and enum names: {items}", dups)

        dups, items = check_dups(slots, classes)
        if items:
            self.logger_warning(f"Overlapping slot and class names: {items}", dups)

        dups, items = check_dups(subsets, classes)
        if items:
            self.logger_warning(f"Overlapping subset and class names: {items}", dups)

        dups, items = check_dups(types, slots)
        if items:
            self.logger_warning(f"Overlapping type and slot names: {items}", dups)

        dups, items = check_dups(subsets, slots)
        if items:
            self.logger_warning(f"Overlapping subset and slot names: {items}", dups)

        dups, items = check_dups(subsets, types)
        if items:
            self.logger_warning(f"Overlapping subset and type names: {items}", dups)

        dups, items = check_dups(enums, slots)
        if items:
            self.logger_warning(f"Overlapping enum and slot names: {items}", dups)

        dups, items = check_dups(subsets, enums)
        if items:
            self.logger_warning(f"Overlapping subset and enum names: {items}", dups)

        # Check over the various enumeration constraints
        for enum in self.schema.enums.values():
            if enum.code_set_version:
                if enum.code_set_tag:
                    self.raise_value_errors(
                        f'Enum: "{enum.name}" cannot have both version and tag',
                        [enum.code_set_version, enum.code_set_tag],
                    )
                if not enum.code_set:
                    self.raise_value_error(
                        f'Enum: "{enum.name}" needs a code set to have a version',
                        enum.name,
                    )
            if enum.code_set_tag:
                if not enum.code_set:
                    self.raise_value_error(f'Enum: "{enum.name}" needs a code set to have a tag', enum.name)
            if enum.pv_formula:
                if not enum.code_set:
                    self.raise_value_error(
                        f'Enum: "{enum.name}" needs a code set to have a formula',
                        enum.name,
                    )
                if enum.permissible_values:
                    self.raise_value_error(
                        f'Enum: "{enum.name}" can have a formula or permissible values but not both',
                        enum.name,
                    )
        for slot in self.schema.slots.values():
            if slot.range and slot.range in self.schema.enums:
                if slot.inlined or slot.inlined_as_list:
                    self.raise_value_error(
                        f'Slot: "{slot.name}" enumerations cannot be inlined',
                        slot.range,
                    )

        # Make the source file relative if it is locally generated
        self.schema_location = self.schema.source_file
        if self.schema.source_file and "://" not in self.schema.source_file:
            self.schema.source_file = os.path.basename(self.schema.source_file)

        # Make sure there is only one tree_root
        tree_root = None
        for cls in self.schema.classes.values():
            if cls.tree_root:
                if tree_root is not None:
                    self.logger.warning(f"Duplicate tree_root: {cls.name} with {tree_root}")
                else:
                    tree_root = cls.name

        self.synopsis = SchemaSynopsis(self.schema)
        errs = self.synopsis.errors()
        if errs:
            print("Warning: The following errors were encountered in the schema")
            for errline in errs:
                print("\t" + errline)
            print()
        for subset, referees in self.synopsis.subsetrefs.items():
            if subset not in self.schema.subsets:
                self.raise_value_error(f"Subset: {subset} is not defined", subset)
        return self.schema

    def validate_item_names(self, typ: str, names: List[str]) -> None:
        # TODO: add a more rigorous syntax check for item names
        for name in names:
            if ":" in name:
                raise self.raise_value_error(f'{typ}: "{name}" - ":" not allowed in identifier', name)

    def merge_enum(self, enum: EnumDefinition, merged_enums: List[EnumDefinitionName]) -> None:
        """
        Merge parent enumeration information into target enum

        :param enum: target enumeration
        :param merged_enums: list of enum names that have been merged. Used to do distal ancestor resolution
        """
        if enum.name not in merged_enums:
            merged_enums.append(enum.name)
            if enum.is_a:
                if enum.is_a in self.schema.enums:
                    self.merge_enum(self.schema.enums[enum.is_a], merged_enums)
                    # merge_enums(self.schema, enum, self.schema.enums[enum.is_a], False)
                else:
                    self.raise_value_error(
                        f'Enum: "{enum.name}" - unknown is_a reference: {enum.is_a}',
                        enum.is_a,
                    )

    def merge_slot(self, slot: SlotDefinition, merged_slots: List[SlotDefinitionName]) -> None:
        """
        Merge parent slot information into target slot

        :param slot: target slot
        :param merged_slots: list of slot names that have been merged.  Used to do a distal ancestor resolution
        """
        if slot.name not in merged_slots:
            if slot.is_a:
                try:
                    if slot.is_a in self.schema.slots:
                        self.merge_slot(self.schema.slots[slot.is_a], merged_slots)
                        merge_slots(slot, self.schema.slots[slot.is_a])
                    else:
                        self.raise_value_error(
                            f'Slot: "{slot.name}" - unknown is_a reference: {slot.is_a}',
                            slot.is_a,
                        )
                except RecursionError:
                    self.raise_value_error(
                        f'Slot: "{slot.name}" - recursive is_a reference: {slot.is_a}',
                        slot.is_a,
                    )

            for mixin in slot.mixins:
                if mixin in self.schema.slots:
                    self.merge_slot(self.schema.slots[mixin], merged_slots)
                    merge_slots(slot, self.schema.slots[mixin])
                else:
                    self.raise_value_error(f'Slot: "{slot.name}" - unknown mixin reference: {mixin}', mixin)
            merged_slots.append(slot.name)

    def merge_class(self, cls: ClassDefinition, merged_classes: List[ClassDefinitionName]) -> None:
        """
        Merge parent class information into target class

        :param cls: target class
        :param merged_classes: list of class names that have been merged. Used to do distal ancestor resolution
        """
        if cls.name not in merged_classes:
            merged_classes.append(cls.name)
            if cls.is_a:
                if cls.is_a in self.schema.classes:
                    self.merge_class(self.schema.classes[cls.is_a], merged_classes)
                    merge_classes(self.schema, cls, self.schema.classes[cls.is_a], False)
                else:
                    self.raise_value_error(
                        f'Class: "{cls.name}" - unknown is_a reference: {cls.is_a}',
                        cls.is_a,
                    )
            for mixin in cls.mixins:
                # Note that apply_to has been injected as a faux mixin, so it gets covered here
                if mixin in self.schema.classes:
                    self.merge_class(self.schema.classes[mixin], merged_classes)
                    merge_classes(self.schema, cls, self.schema.classes[mixin], True)
                else:
                    self.raise_value_error(f'Class: "{cls.name}" - unknown mixin reference: {mixin}', mixin)

    def process_slot_usage_definitions(self):
        """
        Slot usages can be used to completely define slots.  Iterate over the class hierarchy finding all slot
        definitions that are introduced strictly as usages and add them to the slots component
        """
        visited: Set[ClassDefinitionName] = set()
        visited_usages: Set[SlotDefinitionName] = set()  # Slots that are or will be mangled

        def located_aliased_parent_slot(owning_class: ClassDefinition, usage_slot: SlotDefinition) -> bool:
            """Determine whether we are overriding an attributes style slot in the parent class
            Preconditions: usage_slot is NOT in schema.slots
            """
            usage_attribute_name = mangled_attribute_name(owning_class.name, usage_slot.name)
            if owning_class.is_a:
                parent_slot_name = mangled_attribute_name(owning_class.is_a, usage_slot.name)
                if parent_slot_name in self.schema.slots or parent_slot_name in visited_usages:
                    usage_slot.is_a = parent_slot_name
                    visited_usages.add(usage_attribute_name)
                    return True
            for mixin in owning_class.mixins:
                mixin_slot_name = mangled_attribute_name(mixin, usage_slot.name)
                if mixin_slot_name in self.schema.slots or mixin_slot_name in visited_usages:
                    usage_slot.is_a = mixin_slot_name
                    visited_usages.add(usage_attribute_name)
                    return True
            return False

        def visit(classname: ClassDefinitionName) -> None:
            cls = self.schema.classes.get(classname)
            if cls and cls.name not in visited:
                if cls.is_a:
                    visit(cls.is_a)
                for mixin in cls.mixins:
                    visit(mixin)
                for slot_usage in values(cls.slot_usage):
                    if slot_usage.alias:
                        self.raise_value_error(
                            f'Class: "{cls.name}" - alias not permitted in slot_usage slot:' f" {slot_usage.alias}"
                        )
                    if not located_aliased_parent_slot(cls, slot_usage):
                        if slot_usage.name not in self.schema.slots:
                            self.logger.info(
                                f'class "{cls.name}" slot "{slot_usage.name}" '
                                f"does not reference an existing slot.  New slot was created."
                            )
                            # TODO: Consider tightening this up and only allowing usages on defined slots
                            self.schema.slots[slot_usage.name] = slot_usage
                        else:
                            # TODO Make sure that the slot_usage.name is legal (occurs in an ancestor of the class
                            pass
                visited.add(classname)

        for classname in self.schema.classes.keys():
            visit(classname)

    def process_slot_usages(self, cls: ClassDefinition) -> None:
        """
        Connect any slot usage items

        :param cls: class to process
        :return: usage item
        """
        for slotname, slot_usage in cls.slot_usage.items():
            if slot_usage.alias:
                self.raise_value_error(
                    f'Class: "{cls.name}" - alias not permitted in slot_usage slot:' f" {slot_usage.alias}"
                )
            # Construct a new slot
            # If we've already assigned a parent, use it

            if slotname in self.schema.slots:
                base_slot = self.schema.slots[slotname]
            else:
                logging.error(f"slot_usage for undefined slot: {slotname}")
                base_slot = None
            parent_slot = self.schema.slots.get(slot_usage.is_a)
            # Follow the ancestry of the class to get the most proximal parent
            if not parent_slot:
                parent_slot = self.slot_definition_for(slotname, cls)
            if not parent_slot and slotname in self.schema.slots:
                parent_slot = self.schema.slots[slotname]

            if not parent_slot:
                # This test is here because it is really easy to break things in the slot merge utilities.  It should
                # stay
                self.logger.error(f'class "{cls.name}" slot "{slotname}" -- error occurred. This should not happen')
            else:
                child_name = slot_usage_name(slotname, cls)
                slot_alias = parent_slot.alias if parent_slot.alias else slotname
            new_slot = SlotDefinition(
                name=child_name,
                alias=slot_alias,
                domain=cls.name,
                is_usage_slot=Bool(True),
                usage_slot_name=slotname,
                owner=cls.name,
                domain_of=[cls.name],
                imported_from=cls.imported_from,
            )

            self.schema.slots[child_name] = new_slot
            merge_slots(
                new_slot,
                slot_usage,
                inheriting=False,
                skip=[
                    "name",
                    "alias",
                    "domain",
                    "is_usage_slot",
                    "usage_slot_name",
                    "owner",
                    "domain_of",
                ],
            )
            # Copy the parent definition.  If there is no parent definition, the slot is being defined
            # locally as a slot_usage
            if parent_slot is not None:
                new_slot.is_a = parent_slot.name
                merge_slots(new_slot, parent_slot)
                # This situation occurs when we are doing chained overrides.  Kludgy, but it works...
                if parent_slot.name in cls.slots:
                    if child_name in cls.slots:
                        del cls.slots[cls.slots.index(child_name)]
                    cls.slots[cls.slots.index(parent_slot.name)] = child_name
                elif child_name not in cls.slots:
                    cls.slots.append(child_name)
            elif not new_slot.range:
                new_slot.range = self.schema.default_range
            # copy base slot metalsot values across, except where already
            # populated/overridden, OR where propagation to induced slots is
            # forbidden (inverses)
            if base_slot is not None:
                for metaslot_name in base_slot.__dict__.keys():
                    current_val = getattr(new_slot, metaslot_name)
                    if not current_val and metaslot_name not in ["inverse"]:
                        new_val = deepcopy(getattr(base_slot, metaslot_name))
                        if new_val:
                            setattr(new_slot, metaslot_name, new_val)

    def merge_type(self, typ: TypeDefinition, merged_types: List[TypeDefinitionName]) -> None:
        """
        Merge parent type information into target type
        :param typ: target type
        :param merged_types: list of type names that have bee merged.
        """
        if typ.name not in merged_types:
            if typ.typeof:
                if typ.typeof in self.schema.types:
                    reftyp = self.schema.types[cast(TypeDefinitionName, typ.typeof)]
                    self.merge_type(reftyp, merged_types)
                    merge_slots(typ, reftyp, [SlotDefinitionName("imported_from")])
                else:
                    self.raise_value_error(
                        f'Type: "{typ.name}" - unknown typeof reference: {typ.typeof}',
                        typ.typeof,
                    )
            merged_types.append(typ.name)

    def schema_errors(self) -> List[str]:
        return self.synopsis.errors() if self.synopsis else ["resolve() must be run before error check"]

    def slot_definition_for(self, slotname: SlotDefinitionName, cls: ClassDefinition) -> Optional[SlotDefinition]:
        """Find the most proximal definition for slotname in the context of cls"""
        if cls.is_a:
            if cls.is_a not in self.schema.classes:
                self.raise_value_error(f"Unknown parent class: {cls.is_a}", cls.is_a)
            for sn in self.schema.classes[cls.is_a].slots:
                slot = self.schema.slots[sn]
                if (slot.usage_slot_name and slotname == slot.usage_slot_name) or (
                    not slot.usage_slot_name and slotname == slot.name
                ):
                    return slot
        for mixin in cls.mixins:
            if mixin not in self.schema.classes:
                self.raise_value_error(f"Unknown mixin class: {mixin}", cls.is_a)
            for sn in self.schema.classes[mixin].slots:
                slot = self.schema.slots[sn]
                if slot.alias and slotname == slot.alias or slotname == slot.name:
                    return slot
        if cls.is_a:
            defn = self.slot_definition_for(slotname, self.schema.classes[cls.is_a])
            if defn:
                return defn
        for mixin in cls.mixins:
            defn = self.slot_definition_for(slotname, self.schema.classes[mixin])
            if defn:
                return defn
        return None

    def check_prefixes(self) -> None:
        """
        Iterate over the entire schema checking all prefixes
        """
        self.check_prefix(self.schema.default_prefix)
        for prefix in self.schema.emit_prefixes:
            self.check_prefix(prefix)
        for typ in self.schema.types.values():
            self.check_prefix(typ.uri)
            for prefix in typ.mappings:
                self.check_prefix(prefix)
            for prefix in typ.id_prefixes:
                self.check_prefix(prefix)
        for slot in self.schema.slots.values():
            self.check_prefix(slot.slot_uri)
            for prefix in slot.mappings:
                self.check_prefix(prefix)
            for prefix in slot.id_prefixes:
                self.check_prefix(prefix)
        for cls in self.schema.classes.values():
            self.check_prefix(cls.class_uri)
            # Class URI's are inserted into mappings -- see line ~#184
            for prefix in cls.mappings:
                if prefix != cls.class_uri:
                    self.check_prefix(prefix)
            for prefix in cls.id_prefixes:
                self.check_prefix(prefix)

    def check_prefix(self, prefix_or_curie_or_uri: str) -> None:
        prefix = self.namespaces.prefix_for(prefix_or_curie_or_uri, case_shift=False)
        if prefix:
            if prefix not in self.namespaces:
                self.logger.warning(f"{TypedNode.yaml_loc(prefix_or_curie_or_uri)}Unrecognized prefix: {prefix}")
                self.namespaces[prefix] = f"http://example.org/UNKNOWN/{prefix}/"
            else:
                case_adjusted_prefix = self.namespaces.prefix_for(prefix_or_curie_or_uri, case_shift=True)
                if case_adjusted_prefix != prefix:
                    self.logger.warning(
                        f"{TypedNode.yaml_loc(prefix_or_curie_or_uri)}"
                        f"Prefix case mismatch - supplied: {prefix} "
                        f"expected: {case_adjusted_prefix}"
                    )

    @staticmethod
    def slot_name_for(slot: SlotDefinition) -> str:
        return underscore(slot.alias if slot.alias else slot.name)

    @staticmethod
    def raise_value_error(error: str, loc_str: Optional[Union[TypedNode, str]] = None) -> None:
        SchemaLoader.raise_value_errors(error, loc_str)

    @staticmethod
    def raise_value_errors(error: str, loc_str: Optional[Union[str, TypedNode, Iterator[TypedNode]]]) -> None:
        if isinstance(loc_str, list):
            locs = "\n".join(TypedNode.yaml_loc(e, suffix="") for e in loc_str)
            raise ValueError(f"{locs} {error}")
        else:
            raise ValueError(f'{TypedNode.yaml_loc(loc_str, suffix="")} {error}')

    def logger_warning(
        self,
        warning: str,
        loc_str: Optional[Union[str, TypedNode, Iterator[TypedNode]]],
    ) -> None:
        if isinstance(loc_str, list):
            locs = "\n\t".join(TypedNode.yaml_loc(e, suffix="") for e in loc_str)
            self.logger.warning(f"{warning}\n\t{locs}")
        else:
            self.logger.warning(f'{warning}\n\t{TypedNode.yaml_loc(loc_str, suffix="")}')

    def _get_base_dir(self, stated_base: str) -> Optional[str]:
        if stated_base:
            return stated_base
        elif self.schema.source_file:
            if "://" in self.schema.source_file:
                parsed_url = urlparse(self.schema.source_file)
                self.schema.source_file = parsed_url.path.rsplit("/", 1)[-1]
                return parsed_url.path.split("/", 1)[0]
            else:
                rval = os.path.dirname(os.path.abspath(self.schema.source_file))
                return rval
        else:
            return None

    def _check_equals_string(self, slot: SlotDefinition):
        if slot.equals_string or slot.equals_string_in:
            # Range "string" mandatory for "equals_string" and "equals_string_in"
            range = slot.range
            if not range:
                # range is not defined --> check default range
                range = self.schema.default_range
            if range != "string":
                self.raise_value_error(
                    f"slot: {slot.name} - 'equals_string' and 'equals_string_in' requires range "
                    f"'string' and not range '{range}'",
                    slot.range,
                )
            if slot.any_of:
                # It is not allowed to use any of and equals_string or equals_string_in in one slot definition,
                # as both are mapped to sh:in in SHACL
                self.raise_value_error(
                    f"slot: {slot.name} - 'equals_string'/'equals_string_in' and 'any_of' are mutually exclusive",
                    slot.name,
                )
