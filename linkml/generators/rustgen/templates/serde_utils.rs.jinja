#[cfg(feature = "serde")]
use serde::{Deserialize, Deserializer};
#[cfg(feature = "serde")]
use serde_value::{Value, ValueDeserializer};
#[cfg(feature = "serde")]
use serde::de::Error;
#[cfg(feature = "serde")]
use std::collections::{BTreeMap, HashMap};

#[cfg(feature = "serde")]
pub trait InlinedPair: Sized {
    type Key: std::hash::Hash + Eq + serde::de::DeserializeOwned + Clone + Ord;
    type Value: serde::de::DeserializeOwned;
    type Error: std::fmt::Display;

    fn from_pair_mapping(k: Self::Key, v: Value) -> Result<Self,Self::Error>;
    fn from_pair_simple(k: Self::Key, v: Value) -> Result<Self,Self::Error>;
    fn extract_key(&self) -> &Self::Key;
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
    deserializer:  D
) -> Result<Vec<T>, D::Error> where D: Deserializer<'de>, T: Deserialize<'de> {
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
    deserializer:  D
) -> Result<Option<Vec<T>>, D::Error> where D: Deserializer<'de>, T: Deserialize<'de> {
    let ast: Value = Value::deserialize(deserializer)?;
    match ast {
        Value::Unit => Ok(None),
        _ => {
            let d = deserialize_primitive_list_or_single_value(ValueDeserializer::<D::Error>::new(ast))?;
            Ok(Some(d))
        }
    }
}
