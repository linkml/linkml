use std::{
    hash::Hash,
    collections::HashMap,
    iter::{Map, IntoIterator},
    ops::{Index, IndexMut},
    slice,
};

/* ------------------------------------------------------------------- *
 *  Immutable view
 * ------------------------------------------------------------------- */

 pub struct ListView<'a, T> {
    inner: &'a [Box<T>],
}

type ViewIter<'a, T> =
    std::iter::Map<
        std::slice::Iter<'a, Box<T>>,
        fn(&'a Box<T>) -> &'a T,
    >;


impl<'a, T> ListView<'a, T> {

    pub fn len(&self) -> usize        { self.inner.len() }
    pub fn is_empty(&self) -> bool    { self.inner.is_empty() }

    pub fn get(&self, i: usize) -> Option<&T> {
        self.inner.get(i).map(|b| &**b)
    }

    pub fn new(inner: &'a [Box<T>]) -> ListView<'a, T> {
        Self { inner : inner }
    }


    pub fn iter(&self) -> ViewIter<'a, T> {
        self.inner.iter().map(debox)
    }
}

/* Index (`view[i]`) */
impl<'a, T> Index<usize> for ListView<'a, T> {
    type Output = T;
    fn index(&self, i: usize) -> &Self::Output { &*self.inner[i] }
}

/* &ListView iteration  (`for x in &view`) */
type Iter<'a, T> = Map<slice::Iter<'a, Box<T>>, fn(&'a Box<T>) -> &'a T>;
fn debox<'a, T>(b: &'a Box<T>) -> &'a T { &**b }

impl<'a, T> IntoIterator for &'a ListView<'a, T> {
    type Item     = &'a T;
    type IntoIter = Iter<'a, T>;
    fn into_iter(self) -> Self::IntoIter { self.inner.iter().map(debox) }
}

/* ------------------------------------------------------------------- *
 *  Mutable view
 * ------------------------------------------------------------------- */

pub struct ListViewMut<'a, T> {
    inner: &'a mut Vec<Box<T>>,
}

impl<'a, T> ListViewMut<'a, T> {
    pub fn len(&self) -> usize        { self.inner.len() }
    pub fn is_empty(&self) -> bool    { self.inner.is_empty() }

    pub fn new(inner: &'a mut Vec<Box<T>>) -> ListViewMut<'a, T> {
        Self { inner : inner }
    }

    pub fn get(&self, i: usize) -> Option<&T> {
        self.inner.get(i).map(|b| &**b)
    }
    pub fn get_mut(&mut self, i: usize) -> Option<&mut T> {
        self.inner.get_mut(i).map(|b| &mut **b)
    }

    pub fn push(&mut self, v: T) {
        self.inner.push(Box::new(v));
    }

    pub fn iter(&self) -> Iter<'_, T> {
        self.inner.iter().map(debox)
    }
    pub fn iter_mut(&mut self) -> IterMut<'_, T> {
        self.inner.iter_mut().map(debox_mut)
    }
}

/* Index / IndexMut */
impl<'a, T> Index<usize> for ListViewMut<'a, T> {
    type Output = T;
    fn index(&self, i: usize) -> &Self::Output { &*self.inner[i] }
}
impl<'a, T> IndexMut<usize> for ListViewMut<'a, T> {
    fn index_mut(&mut self, i: usize) -> &mut Self::Output { &mut *self.inner[i] }
}

/* &mut ListViewMut iteration (`for x in &mut view`) */
fn debox_mut<'a, T>(b: &'a mut Box<T>) -> &'a mut T { &mut **b }
type IterMut<'a, T> = Map<slice::IterMut<'a, Box<T>>, fn(&'a mut Box<T>) -> &'a mut T>;

impl<'a, T> IntoIterator for &'a ListViewMut<'a, T> {
    type Item     = &'a T;
    type IntoIter = Iter<'a, T>;
    fn into_iter(self) -> Self::IntoIter { self.inner.iter().map(debox) }
}
impl<'a, T> IntoIterator for &'a mut ListViewMut<'a, T> {
    type Item     = &'a mut T;
    type IntoIter = IterMut<'a, T>;
    fn into_iter(self) -> Self::IntoIter { self.inner.iter_mut().map(debox_mut) }
}


pub struct MapView<'a, K, V> {
    inner: &'a HashMap<K, Box<V>>,
}

impl<'a, K: Eq + Hash, V> MapView<'a, K, V> {
    /* basic info */
    pub fn len(&self) -> usize        { self.inner.len() }
    pub fn is_empty(&self) -> bool    { self.inner.is_empty() }

    /* look-ups */
    pub fn get(&self, k: &K) -> Option<&V> {
        self.inner.get(k).map(debox)
    }

    pub fn new(inner: &'a HashMap<K, Box<V>>)  -> Self {
        Self { inner : inner }
    }

    pub fn iter(&self) -> impl Iterator<Item = (&K, &V)> + '_ {
        self.inner.iter().map(as_pair)
    }

}

/* &MapView iteration */
type MapIter<'a, K, V> =
    Map<std::collections::hash_map::Iter<'a, K, Box<V>>, fn((&'a K,&'a Box<V>)) -> (&'a K,&'a V)>;

fn as_pair<'a, K, V>((k, v): (&'a K, &'a Box<V>)) -> (&'a K, &'a V) { (k, &**v) }

impl<'a, K: Eq + Hash, V> IntoIterator for &'a MapView<'a, K, V> {
    type Item     = (&'a K, &'a V);
    type IntoIter = MapIter<'a, K, V>;
    fn into_iter(self) -> Self::IntoIter { self.inner.iter().map(as_pair) }
}

/* ------------------------------- mutable view ---------------------- */
pub struct MapViewMut<'a, K, V> {
    inner: &'a mut HashMap<K, Box<V>>,
}

impl<'a, K: Eq + Hash, V> MapViewMut<'a, K, V> {
    /* same basic info */
    pub fn len(&self) -> usize        { self.inner.len() }
    pub fn is_empty(&self) -> bool    { self.inner.is_empty() }

    /* look-ups */
    pub fn get(&self,  k: &K) -> Option<&V>       { self.inner.get(k).map(debox) }
    pub fn get_mut(&mut self, k: &K) -> Option<&mut V> { self.inner.get_mut(k).map(debox_mut) }

    /* insertion / removal */
    pub fn insert(&mut self, k: K, v: V) -> Option<V> {
        self.inner.insert(k, Box::new(v)).map(|old| *old)
    }
    pub fn remove(&mut self, k: &K) -> Option<V> {
        self.inner.remove(k).map(|b| *b)
    }

    /* iterators */
    pub fn iter<'b>(&'b self) -> MapIter<'b, K, V> {
        self.inner.iter().map(as_pair)
    }
    pub fn iter_mut<'b>(&'b mut self) -> MapIterMut<'b, K, V> {
        self.inner.iter_mut().map(as_pair_mut)
    }
}

/* &mut MapViewMut iteration */
type MapIterMut<'a, K, V> =
    Map<std::collections::hash_map::IterMut<'a, K, Box<V>>,
        fn((&'a K,&'a mut Box<V>)) -> (&'a K,&'a mut V)>;

fn as_pair_mut<'a, K, V>((k, v): (&'a K, &'a mut Box<V>)) -> (&'a K, &'a mut V) { (k, &mut **v) }

impl<'a, K: Eq + Hash, V> IntoIterator for &'a mut MapViewMut<'a, K, V> {
    type Item     = (&'a K, &'a mut V);
    type IntoIter = MapIterMut<'a, K, V>;
    fn into_iter(self) -> Self::IntoIter { self.inner.iter_mut().map(as_pair_mut) }
}
/* also allow &MapViewMut to iterate immutably */
impl<'a, K: Eq + Hash, V> IntoIterator for &'a MapViewMut<'a, K, V> {
    type Item     = (&'a K, &'a V);
    type IntoIter = MapIter<'a, K, V>;
    fn into_iter(self) -> Self::IntoIter { self.inner.iter().map(as_pair) }
}


pub trait MapRef<'l, K, V> {
    fn get(&self, k: &K) -> Option<&V>;
    fn len(&self) -> usize;
    fn is_empty(&self) -> bool { self.len() == 0 }

    type Iter<'a>: Iterator<Item = (&'a K, &'a V)>
    where
        Self: 'a,
        K: 'a,
        V: 'a;

    fn iter(&self) -> Self::Iter<'_>;

    fn to_any(self) -> MapAny<'l, K, V>
    where
        Self: Sized;        // keeps it object-safe enough for static dispatch
}


/* NEW — borrowed map */
impl<'a, K: Eq + Hash, V> MapRef<'a, K, V> for &'a HashMap<K, V> {
    fn get(&self, k: &K) -> Option<&V> { (*self).get(k) }
    fn len(&self) -> usize             { (*self).len() }

    type Iter<'b> = std::collections::hash_map::Iter<'b, K, V>
    where
        Self: 'b,
        K: 'b,
        V: 'b;

    fn iter(&self) -> Self::Iter<'a> {
        (*self).iter()
    }
    fn to_any(self) -> MapAny<'a, K, V>
    where
        Self: Sized
     {
        MapAny::Hash(self)
    }
}

/* ---- impl for your borrowing MapView ---------------------------- */
impl<'a, K: std::hash::Hash + Eq, V> MapRef<'a, K, V> for MapView<'a, K, V> {
    fn get(&self, k: &K) -> Option<&V> { self.inner.get(k).map(|b| &**b) }
    fn len(&self) -> usize { self.inner.len() }

    type Iter<'b> =
        std::iter::Map<
            std::collections::hash_map::Iter<'b, K, Box<V>>,
            fn((&'b K,&'b Box<V>)) -> (&'b K,&'b V)
        > where K: 'b, V: 'b, Self: 'b;

    fn iter(&self) -> Self::Iter<'_> {
        fn as_pair<'b, K, V>((k, v): (&'b K, &'b Box<V>)) -> (&'b K, &'b V) { (k, &**v) }
        self.inner.iter().map(as_pair)
    }
    fn to_any(self) -> MapAny<'a, K, V>
    where
        Self: Sized
     {
        MapAny::View(MapView { inner : self.inner })
    }
}



pub trait SeqRef<'l, T> {
    /// Immutable iterator (`for x in seq.iter()`)
    type Iter<'a>: Iterator<Item = &'a T> + ExactSizeIterator
    where
        Self: 'a,
        T: 'a;

    /// Number of elements
    fn len(&self) -> usize;

    /// Immutable indexing
    fn get(&self, i: usize) -> Option<&T>;

    /// Borrowing iterator
    fn iter(&self) -> Self::Iter<'l>;

    /// Convenience
    fn is_empty(&self) -> bool { self.len() == 0 }

    fn to_any(self) -> ListAny<'l, T>
    where
        Self: Sized;
}


impl<'l, T> SeqRef<'l, T> for &'l Vec<T> {
    type Iter<'a> = slice::Iter<'a, T> where T: 'a, Self: 'a;

    fn len(&self) -> usize              { Vec::len(self) }
    fn get(&self, i: usize) -> Option<&T> { self.as_slice().get(i) }
    fn iter(&self) -> Self::Iter<'l>    { self.as_slice().iter() }
    fn to_any(self) -> ListAny<'l, T>
    where
        Self: Sized,
    {
        ListAny::Vec(self)
    }
}


impl<'a, T> SeqRef<'a, T> for ListView<'a, T> {
    type Iter<'b> = Iter<'b, T> where Self: 'b, T: 'b;

    fn len(&self) -> usize              { self.inner.len() }
    fn get(&self, i: usize) -> Option<&T> { self.inner.get(i).map(debox) }
    fn iter(&self) -> Self::Iter<'a>    { self.inner.iter().map(debox) }
    fn to_any(self) -> ListAny<'a, T>
    where
        Self: Sized,
    {
        ListAny::View(ListView { inner:  self.inner })
    }
}

pub enum MapAny<'a, K, V> {
    Hash(&'a std::collections::HashMap<K, V>),   // &HashMap
    View(MapView<'a, K, V>),               // MapView (already borrows)
}

impl<'a, K: Eq + std::hash::Hash, V> MapRef<'a, K, V>
    for MapAny<'a, K, V>
{
    type Iter<'b> =
        std::boxed::Box<dyn Iterator<Item = (&'b K, &'b V)> + 'b>
        where Self: 'b, K: 'b, V: 'b;

    fn len(&self) -> usize {
        match self {
            Self::Hash(m) => m.len(),
            Self::View(v) => v.len(),
        }
    }
    fn get(&self, k: &K) -> Option<&V> {
        match self {
            Self::Hash(m) => m.get(k),
            Self::View(v) => v.get(k),
        }
    }
    fn iter(&self) -> Self::Iter<'_> {
        match self {
            Self::Hash(m) => Box::new(m.iter()),
            Self::View(v) => Box::new(v.iter()),
        }
    }
    fn to_any(self) -> MapAny<'a, K, V>
        where
            Self: Sized,
             {
        match self {
            Self::Hash(m) => MapAny::Hash(m),
            Self::View(v) => MapAny::View(v),
         }
    }
}


pub enum ListIter<'a, T> {
    Vec  (std::slice::Iter<'a, T>),
    View (ViewIter<'a, T>),
}

impl<'a, T> Iterator for ListIter<'a, T> {
    type Item = &'a T;
    fn next(&mut self) -> Option<Self::Item> {
        match self {
            Self::Vec(it)  => it.next(),
            Self::View(it) => it.next(),
        }
    }
    fn size_hint(&self) -> (usize, Option<usize>) {
        match self {
            Self::Vec(it)  => it.size_hint(),
            Self::View(it) => it.size_hint(),
        }
    }
}

impl<'a, T> ExactSizeIterator for ListIter<'a, T> {
    fn len(&self) -> usize {
        match self {
            Self::Vec(it)  => it.len(),
            Self::View(it) => it.len(),
        }
    }
}

pub enum ListAny<'a, T> {
    Vec(&'a Vec<T>),                  // &Vec<T>
    View(ListView<'a, T>),        // ListView (already borrows)
}

/* ------------------------------------------------------------------ *
 *  SeqRef implementation
 * ------------------------------------------------------------------ */
impl<'a, T> SeqRef<'a, T> for ListAny<'a, T> {
    type Iter<'x> = ListIter<'x, T> where Self: 'x, T: 'x;
    //type Iter<'b> =
    //    std::boxed::Box<dyn Iterator<Item = &'b T> + ExactSizeIterator + 'b>
    //    where Self: 'b, T: 'b;

    fn len(&self) -> usize {
        match self {
            Self::Vec(v)  => v.len(),
            Self::View(v) => v.len(),
        }
    }
    fn get(&self, i: usize) -> Option<&T> {
        match self {
            Self::Vec(v)  => v.get(i),
            Self::View(v) => v.get(i),
        }
    }
    fn iter(&self) -> Self::Iter<'a> {
        match self {
            Self::Vec(v)  => ListIter::Vec(v.iter()),
            Self::View(v) => ListIter::View(v.iter()),
        }
    }
    fn to_any(self) -> ListAny<'a, T>
    where
        Self: Sized,
         {
            match self {
                Self::Vec(v)  => ListAny::Vec(v),
                Self::View(v) => ListAny::View(v),
            }
          }
}
