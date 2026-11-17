use std::collections::HashMap;

use crate::direction::Direction;

pub struct Room {
    pub id: String,
    pub name: String,
    pub description: String,
    pub exits: HashMap<Direction, String>,
}

impl Room {
    pub fn new(id: String, name: String, description: String) -> Self {
        Self {
            id,
            name,
            description,
            exits: HashMap::new(),
        }
    }

    pub fn add_exit(&mut  self, direction: Direction, room_id: String) {
        self.exits.insert(direction, room_id);
    }

    pub fn has_exit(&self, direction: &Direction) -> bool {
        self.exits.contains_key(direction)
    }

    pub fn get_exit(&self, direction: &Direction) -> Option<&String> {
        self.exits.get(direction)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_room() {
        let mut room = Room::new(
            String::from("room_01"),
            String::from("Entrée du château"),
            String::from("Une grande salle."),
        );

        room.add_exit(
            Direction::North,
            String::from("room_02"),
        );

        assert_eq!(room.id, "room_01");
        assert_eq!(
            room.exits.get(&Direction::North),
            Some(&String::from("room_02"))
        );
    }

    #[test]
    fn test_has_exit() {
        let mut room = Room::new(
            "forest".to_string(),
            "La forêt".to_string(),
            "Une forêt mystérieuse".to_string(),
        );

        room.add_exit(Direction::North, "castle".to_string());

        assert!(room.has_exit(&Direction::North));
        assert!(!room.has_exit(&Direction::South));
    }

    #[test]
    fn test_get_exit() {
        let mut room = Room::new(
            "forest".to_string(),
            "La forêt".to_string(),
            "Une forêt mystérieuse".to_string(),
        );

        room.add_exit(Direction::North, "castle".to_string());

        assert_eq!(
            room.get_exit(&Direction::North),
            Some(&"castle".to_string())
        );

        assert_eq!(
            room.get_exit(&Direction::South),
            None
        );
    }

    #[test]
    fn test_move_through_exit() {
        let mut room = Room::new(
            "forest".to_string(),
            "La forêt".to_string(),
            "Une forêt mystérieuse".to_string(),
        );

        room.add_exit(Direction::North, "castle".to_string());

        let mut character = crate::character::Character::new(
            "player_1".to_string(),
            "Anna".to_string(),
            "forest".to_string(),
        );

        if let Some(destination) = room.get_exit(&Direction::North) {
            character.move_to(destination.clone());
        }

        assert_eq!(character.room_id, "castle");
    }
}