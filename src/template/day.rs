use std::{error::Error, fmt::Display, str::FromStr};

#[cfg(feature = "today")]
use chrono::{Datelike, FixedOffset, Utc};

#[cfg(feature = "today")]
const SERVER_UTC_OFFSET: i32 = -5;

/// A valid advent day number (i.e. an integer in range 1 to 25).
///
/// # Display
/// This value displays as a two digit number.
///
/// ```
/// # use advent_of_code::Day;
/// let day = Day::new(8).unwrap();
/// assert_eq!(day.to_string(), "08")
/// ```
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct Day(u8);

impl Day {
    /// Creates a `Day` from provided value if in valid range, `None` otherwise.
    pub fn new(day: u8) -> Option<Self> {
        (1..=25).contains(&day).then_some(Self(day))
    }

    // Not part of public API
    #[doc(hidden)]
    pub const fn __new_unchecked(day: u8) -> Self {
        Self(day)
    }

    /// Convert `Day` into `u8`
    pub fn into_inner(self) -> u8 {
        self.0
    }
}

#[cfg(feature = "today")]
impl Day {
    /// Returns current day if in valid range
    pub fn today() -> Option<Self> {
        let offset = FixedOffset::east_opt(SERVER_UTC_OFFSET * 3600)?;
        let today = Utc::now().with_timezone(&offset);

        (today.month() == 12 && (1..=25).contains(&today.day()))
            .then(|| u8::try_from(today.day()).ok())
            .flatten()
            .and_then(Self::new)
    }
}

impl Display for Day {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:02}", self.0)
    }
}

impl PartialEq<u8> for Day {
    fn eq(&self, other: &u8) -> bool {
        self.0.eq(other)
    }
}

impl PartialOrd<u8> for Day {
    fn partial_cmp(&self, other: &u8) -> Option<std::cmp::Ordering> {
        self.0.partial_cmp(other)
    }
}

impl FromStr for Day {
    type Err = DayFromStrError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        s.parse::<u8>()
            .ok()
            .and_then(Self::new)
            .ok_or(DayFromStrError)
    }
}

#[derive(Debug)]
pub struct DayFromStrError;

impl Error for DayFromStrError {}

impl Display for DayFromStrError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Expecting a day number between 1 and 25")
    }
}

/// Iterator yielding every day of AoC
pub fn all_days() -> AllDays {
    AllDays::new()
}

pub struct AllDays {
    current: u8,
}

impl Default for AllDays {
    fn default() -> Self {
        Self::new()
    }
}

impl AllDays {
    pub fn new() -> Self {
        Self { current: 1 }
    }
}

impl Iterator for AllDays {
    type Item = Day;

    fn next(&mut self) -> Option<Self::Item> {
        (1..=25).contains(&self.current).then(|| {
            let day = Day(self.current);
            self.current += 1;
            day
        })
    }
}

/// Create `Day` value in const context
#[macro_export]
macro_rules! day {
    ($day:expr) => {{
        const _: () = assert!(
            $day >= 1 && $day <= 25,
            concat!(
                "invalid day number `",
                stringify!($day),
                "`, expecting a value between 1 and 25"
            )
        );
        $crate::template::Day::__new_unchecked($day)
    }};
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn all_days_iterator() {
        let all: Vec<_> = all_days().collect();
        assert_eq!(all.len(), 25);
        assert_eq!(all[0], Day::new(1).unwrap());
        assert_eq!(all[24], Day::new(25).unwrap());
    }

    #[test]
    fn day_display() {
        fn day_display() {
            assert_eq!(Day::new(1).unwrap().to_string(), "01");
            assert_eq!(Day::new(25).unwrap().to_string(), "25");
        }
    }

    #[test]
    fn day_from_str() {
        assert_eq!("12".parse::<Day>().unwrap(), Day::new(12).unwrap());
        assert!("0".parse::<Day>().is_err());
        assert!("26".parse::<Day>().is_err());
    }
}
