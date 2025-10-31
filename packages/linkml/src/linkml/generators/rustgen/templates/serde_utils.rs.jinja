#[cfg(feature = "serde")]
use serde::{
    de::{DeserializeOwned, IntoDeserializer},
    Deserialize,
    Deserializer,
    Serialize,
    Serializer,
};
#[cfg(feature = "serde")]
use serde::de::Error;
#[cfg(feature = "serde")]
use serde_value::{to_value, Value, ValueDeserializer};
#[cfg(feature = "serde")]
use std::collections::{BTreeMap, HashMap};
#[cfg(all(feature = "serde", feature = "pyo3"))]
use pyo3::prelude::*;
#[cfg(all(feature = "serde", feature = "pyo3"))]
use pyo3::types::{PyAny, PyDict, PyList, PyTuple};

#[cfg(feature = "serde")]
pub trait InlinedPair: Sized {
    type Key: std::hash::Hash + Eq + serde::de::DeserializeOwned + Clone + Ord;
    type Value: serde::de::DeserializeOwned;
    type Error: std::fmt::Display;

    fn from_pair_mapping(k: Self::Key, v: Value) -> Result<Self,Self::Error>;
    fn from_pair_simple(k: Self::Key, v: Value) -> Result<Self,Self::Error>;
    fn extract_key(&self) -> &Self::Key;

    fn simple_value(&self) -> Option<&Self::Value> {
        None
    }

    fn compact_value(&self) -> Option<Value> {
        None
    }
}

#[cfg(feature = "serde")]
impl<T> InlinedPair for Box<T>
where
    T: InlinedPair + ?Sized,           // allow unsized boxes too
{
    type Key   = T::Key;
    type Value = T::Value;
    type Error = T::Error;

    #[inline]
    fn from_pair_mapping(k: Self::Key, v: Value) -> Result<Self, Self::Error> {
        T::from_pair_mapping(k, v).map(|x| Box::new(x))
    }

    #[inline]
    fn from_pair_simple(k: Self::Key, v: Value) -> Result<Self, Self::Error>  {
        T::from_pair_simple(k, v).map(|x| Box::new(x))
    }

    #[inline]
    fn extract_key(&self) -> &Self::Key {
        T::extract_key(self)
     }

    fn simple_value(&self) -> Option<&Self::Value> {
        self.as_ref().simple_value()
    }

    fn compact_value(&self) -> Option<Value> {
        self.as_ref().compact_value()
    }

}

#[cfg(feature = "serde")]
#[allow(dead_code)]
pub fn deserialize_inlined_dict_list<'de, D, T>(de: D) -> Result<Vec<T>, D::Error>
where
    D: Deserializer<'de>,
    T: InlinedPair,
{
    let raw: BTreeMap<T::Key, Value> = BTreeMap::deserialize(de)?;
    raw.into_iter().map(|(k, v)| {
        let obj = T::from_pair_mapping(k.clone(), v).map_err(D::Error::custom)?;
        Ok(obj)
    }).collect()

}

#[cfg(feature = "serde")]
pub fn deserialize_inlined_dict_map<'de, D, T>(
    de: D,
) -> Result<HashMap<T::Key, T>, D::Error>
where
    D: Deserializer<'de>,
    T: InlinedPair + Deserialize<'de>,
{

    // Parse into a generic AST once
    let ast: Value = Value::deserialize(de)?;

    match ast {
        // ---------- { key : value } form ----------
        Value::Map(m) => {
            let mut out = HashMap::with_capacity(m.len());
            for (k_ast, v_ast) in m {
                // 1) convert key and value separately
                let key: T::Key = Deserialize::deserialize(
                    ValueDeserializer::<D::Error>::new(k_ast)
                ).map_err(D::Error::custom)?;


                // ----------------- decide by the *value* shape
                let obj = match v_ast {
                    // (1) full object (mapping) -> deserialize directly
                    Value::Map(_) => {
                        let m: Value = Deserialize::deserialize(
                            ValueDeserializer::<D::Error>::new(v_ast)
                        ).map_err(D::Error::custom)?;
                        T::from_pair_mapping(key.clone(), m).map_err(D::Error::custom)?
                    }
                    other => {
                        T::from_pair_simple(key.clone(), other).map_err(D::Error::custom)?
                    }
                };


                out.insert(key, obj);
            }
            Ok(out)
        }

        // ---------- [ value, ... ] form -------------
        Value::Seq(seq) => {
            let mut out = HashMap::with_capacity(seq.len());
            for v_ast in seq {
                let val: T = Deserialize::deserialize(
                    ValueDeserializer::<D::Error>::new(v_ast)
                ).map_err(D::Error::custom)?;

                let key = val.extract_key().clone();
                if out.insert(key, val).is_some() {
                    return Err(D::Error::custom("duplicate key"));
                }
            }
            Ok(out)
        }

        _ => Err(D::Error::custom("expected mapping or sequence")),
    }
}

#[cfg(feature = "serde")]
pub fn deserialize_inlined_dict_map_optional<'de, D, T>(
    de: D,
) -> Result<Option<HashMap<T::Key, T>>, D::Error>
where
    D: Deserializer<'de>,
    T: InlinedPair + Deserialize<'de>,
{
    let ast: Value = Value::deserialize(de)?;
    match ast {
        Value::Unit => Ok(None),
        Value::Map(_) | Value::Seq(_) => {
            let map = deserialize_inlined_dict_map(ValueDeserializer::<D::Error>::new(ast))?;
            Ok(Some(map))
        }
        _ => Err(D::Error::custom("expected mapping, sequence, or unit")),
    }
}


#[cfg(feature = "serde")]
#[allow(dead_code)]
pub fn deserialize_inlined_dict_list_optional<'de, D, T>(
    de: D,
) -> Result<Option<Vec<T>>, D::Error>
where
    D: Deserializer<'de>,
    T: InlinedPair + Deserialize<'de>,
{
    let ast: Value = Value::deserialize(de)?;
    match ast {
        Value::Unit => Ok(None),
        Value::Map(_) => {
            let list = deserialize_inlined_dict_list(ValueDeserializer::<D::Error>::new(ast))?;
            Ok(Some(list))
        }
        Value::Seq(seq) => {
            let mut out = Vec::with_capacity(seq.len());
            for v_ast in seq {
                let val: T = Deserialize::deserialize(ValueDeserializer::<D::Error>::new(v_ast))
                    .map_err(D::Error::custom)?;
                out.push(val);
            }
            Ok(Some(out))
        }
        _ => Err(D::Error::custom("expected mapping, sequence, or unit")),
    }
}

pub fn deserialize_primitive_list_or_single_value<'de, D, T>(
    deserializer: D
) -> Result<Vec<T>, D::Error>
where
    D: Deserializer<'de>,
    T: Deserialize<'de>,
{
    let ast: Value = Value::deserialize(deserializer)?;
    match ast {
        Value::Seq(seq) => {
            seq.into_iter()
                .map(|v| T::deserialize(ValueDeserializer::<D::Error>::new(v)))
                .collect()
        }
        Value::Unit => Ok(vec![]),
        other => {
            let single_value: T = Deserialize::deserialize(
                ValueDeserializer::<D::Error>::new(other)
            ).map_err(D::Error::custom)?;
            Ok(vec![single_value])
        }
    }
}


pub fn deserialize_primitive_list_or_single_value_optional<'de, D, T>(
    deserializer: D
) -> Result<Option<Vec<T>>, D::Error>
where
    D: Deserializer<'de>,
    T: Deserialize<'de>,
{
    let ast: Value = Value::deserialize(deserializer)?;
    match ast {
        Value::Unit => Ok(None),
        _ => {
            let d = deserialize_primitive_list_or_single_value(ValueDeserializer::<D::Error>::new(ast))?;
            Ok(Some(d))
        }
    }
}

#[cfg(all(feature = "serde", feature = "pyo3"))]
fn py_any_to_value(bound: &Bound<'_, PyAny>) -> PyResult<Value> {
    if bound.is_none() {
        return Ok(Value::Unit);
    }

    if let Ok(b) = bound.extract::<bool>() {
        return Ok(Value::Bool(b));
    }

    if let Ok(i) = bound.extract::<i64>() {
        return Ok(Value::I64(i));
    }

    if let Ok(f) = bound.extract::<f64>() {
        return Ok(Value::F64(f));
    }

    if let Ok(s) = bound.extract::<String>() {
        return Ok(Value::String(s));
    }

    if let Ok(dict_obj) = bound.getattr("__dict__") {
        if let Ok(dict) = dict_obj.downcast::<PyDict>() {
            let mut map: BTreeMap<Value, Value> = BTreeMap::new();
            for (k, v) in dict.iter() {
                let key_str: String = k.extract()?;
                let val = py_any_to_value(&v)?;
                map.insert(Value::String(key_str), val);
            }
            return Ok(Value::Map(map));
        }
    }

    if let Ok(dict) = bound.downcast::<PyDict>() {
        let mut map: BTreeMap<Value, Value> = BTreeMap::new();
        for (k, v) in dict.iter() {
            let key_str: String = k.extract()?;
            let val = py_any_to_value(&v)?;
            map.insert(Value::String(key_str), val);
        }
        return Ok(Value::Map(map));
    }

    if let Ok(list) = bound.downcast::<PyList>() {
        let mut items = Vec::with_capacity(list.len());
        for item in list.iter() {
            items.push(py_any_to_value(&item)?);
        }
        return Ok(Value::Seq(items));
    }

    if let Ok(tuple) = bound.downcast::<PyTuple>() {
        let mut items = Vec::with_capacity(tuple.len());
        for item in tuple.iter() {
            items.push(py_any_to_value(&item)?);
        }
        return Ok(Value::Seq(items));
    }

    Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
        "unsupported value type for conversion",
    ))
}

#[cfg(feature = "serde")]
#[allow(dead_code)]
pub fn serialize_inlined_dict_map<S, T>(
    value: &HashMap<T::Key, T>,
    serializer: S,
) -> Result<S::Ok, S::Error>
where
    S: Serializer,
    T: InlinedPair + Serialize,
    T::Key: Serialize + Clone + Ord,
    T::Value: Serialize,
{
    let mut ordered: BTreeMap<T::Key, &T> = BTreeMap::new();
    for (k, v) in value.iter() {
        ordered.insert(k.clone(), v);
    }

    let mut as_values: BTreeMap<T::Key, Value> = BTreeMap::new();
    for (k, v) in ordered.iter() {
        if let Some(simple) = v.simple_value() {
            let val = to_value(simple)
                .map_err(|e| <S::Error as serde::ser::Error>::custom(e))?;
            as_values.insert((*k).clone(), val);
            continue;
        }
        if let Some(compact) = v.compact_value() {
            as_values.insert((*k).clone(), compact);
            continue;
        }
        let val = to_value(*v)
            .map_err(|e| <S::Error as serde::ser::Error>::custom(e))?;
        as_values.insert((*k).clone(), val);
    }
    as_values.serialize(serializer)
}

#[cfg(feature = "serde")]
#[allow(dead_code)]
pub fn serialize_inlined_dict_map_optional<S, T>(
    value: &Option<HashMap<T::Key, T>>,
    serializer: S,
) -> Result<S::Ok, S::Error>
where
    S: Serializer,
    T: InlinedPair + Serialize,
    T::Key: Serialize + Clone + Ord,
    T::Value: Serialize,
{
    match value {
        Some(map) => serialize_inlined_dict_map(map, serializer),
        None => serializer.serialize_none(),
    }
}

#[cfg(feature = "serde")]
#[allow(dead_code)]
pub fn serialize_inlined_dict_list<S, T>(
    value: &Vec<T>,
    serializer: S,
) -> Result<S::Ok, S::Error>
where
    S: Serializer,
    T: InlinedPair + Serialize,
    T::Key: Serialize + Clone + Ord,
    T::Value: Serialize,
{
    let mut ordered: BTreeMap<T::Key, &T> = BTreeMap::new();
    for item in value.iter() {
        ordered.insert(item.extract_key().clone(), item);
    }

    let mut as_values: BTreeMap<T::Key, Value> = BTreeMap::new();
    for (k, v) in ordered.iter() {
        if let Some(simple) = v.simple_value() {
            let val = to_value(simple)
                .map_err(|e| <S::Error as serde::ser::Error>::custom(e))?;
            as_values.insert((*k).clone(), val);
            continue;
        }
        if let Some(compact) = v.compact_value() {
            as_values.insert((*k).clone(), compact);
            continue;
        }
        let val = to_value(*v)
            .map_err(|e| <S::Error as serde::ser::Error>::custom(e))?;
        as_values.insert((*k).clone(), val);
    }
    as_values.serialize(serializer)
}

#[cfg(feature = "serde")]
#[allow(dead_code)]
pub fn serialize_inlined_dict_list_optional<S, T>(
    value: &Option<Vec<T>>,
    serializer: S,
) -> Result<S::Ok, S::Error>
where
    S: Serializer,
    T: InlinedPair + Serialize,
    T::Key: Serialize + Clone + Ord,
    T::Value: Serialize,
{
    match value {
        Some(items) => serialize_inlined_dict_list(items, serializer),
        None => serializer.serialize_none(),
    }
}

#[cfg(feature = "serde")]
#[allow(dead_code)]
pub fn serialize_primitive_list_or_single_value<S, T>(
    value: &Vec<T>,
    serializer: S,
) -> Result<S::Ok, S::Error>
where
    S: Serializer,
    T: Serialize,
{
    match value.as_slice() {
        [single] => single.serialize(serializer),
        _ => value.serialize(serializer),
    }
}

#[cfg(feature = "serde")]
#[allow(dead_code)]
pub fn serialize_primitive_list_or_single_value_optional<S, T>(
    value: &Option<Vec<T>>,
    serializer: S,
) -> Result<S::Ok, S::Error>
where
    S: Serializer,
    T: Serialize,
{
    match value {
        Some(v) => serialize_primitive_list_or_single_value(v, serializer),
        None => serializer.serialize_none(),
    }
}

#[cfg(all(feature = "serde", feature = "pyo3"))]
pub fn deserialize_py_any<'py, T>(bound: &Bound<'py, PyAny>) -> PyResult<T>
where
    T: DeserializeOwned,
{
    let value = py_any_to_value(bound)?;
    let de = value.into_deserializer();
    match serde_path_to_error::deserialize(de) {
        Ok(ok) => Ok(ok),
        Err(err) => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            format!("at `{}`: {}", err.path(), err.inner()),
        )),
    }
}

#[cfg(feature = "pyo3")]
pub struct PyValue<T>(pub T);

#[cfg(feature = "pyo3")]
impl<T> PyValue<T> {
    pub fn into_inner(self) -> T {
        self.0
    }
}

#[cfg(all(feature = "pyo3", feature = "stubgen"))]
impl<T> ::pyo3_stub_gen::PyStubType for PyValue<T>
where
    T: ::pyo3_stub_gen::PyStubType,
{
    fn type_output() -> ::pyo3_stub_gen::TypeInfo {
        T::type_output()
    }
}

#[cfg(all(feature = "pyo3", feature = "serde"))]
impl<'py, T> FromPyObject<'py> for PyValue<T>
where
    T: DeserializeOwned,
{
    fn extract_bound(ob: &Bound<'py, PyAny>) -> PyResult<Self> {
        deserialize_py_any(ob).map(PyValue)
    }
}
