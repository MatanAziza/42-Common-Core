#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Direction {
    North,
    South,
    East,
    West,
    Up,
    Down,
}

impl Direction {
    pub fn opposite(&self) -> Self {
        match self {
            Direction::North => Direction::South,
            Direction::South => Direction::North,
            Direction::East => Direction::West,
            Direction::West => Direction::East,
            Direction::Up => Direction::Down,
            Direction::Down => Direction::Up,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_opposite() {
        assert_eq!(Direction::North.opposite(), Direction::South);
        assert_eq!(Direction::South.opposite(), Direction::North);

        assert_eq!(Direction::East.opposite(), Direction::West);
        assert_eq!(Direction::West.opposite(), Direction::East);

        assert_eq!(Direction::Up.opposite(), Direction::Down);
        assert_eq!(Direction::Down.opposite(), Direction::Up);
    }
}