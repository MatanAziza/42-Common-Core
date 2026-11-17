use std::collections::HashMap;
use crate::room::Room;
use crate::direction::Direction;

pub struct World {
    pub rooms: HashMap<String, Room>,
}

impl World {
    pub fn new() -> Self {
        Self {
            rooms: HashMap::new(),
        }
    }

    pub fn add_room(&mut self, room: Room) {
        self.rooms.insert(room.id.clone(), room);
    }

    pub fn get_room(&self, room_id: &str) -> Option<&Room> {
        self.rooms.get(room_id)
    }

    pub fn room_exists(&self, room_id: &str) -> bool {
        self.rooms.contains_key(room_id)
    }

    pub fn connect_rooms(
        &mut self,
        from_id: &str,
        direction: Direction,
        to_id: &str,
    ) -> bool {
        if !self.room_exists(from_id) || !self.room_exists(to_id) {
            return false;
        }

        if let Some(room) = self.rooms.get_mut(from_id) {
            room.add_exit(direction, to_id.to_string());
            return true;
        }
        false
    }

    pub fn connect_rooms_bidirectional(
        &mut self,
        from_id: &str,
        direction: Direction,
        to_id: &str,
    ) -> bool {
        if !self.room_exists(from_id) || !self.room_exists(to_id) {
            return false;
        }

        if from_id == to_id {
            return false;
        }

        self.connect_rooms(from_id, direction, to_id);
        self.connect_rooms(to_id, direction.opposite(), from_id);

        true
    }

    pub fn move_character(
        &self,
        character: &mut crate::character::Character,
        direction: &Direction,
    ) -> bool {
        let Some(room) = self.get_room(&character.room_id) else {
            return false;
        };

        let Some(destination) = room.get_exit(direction) else {
            return false;
        };

        if !self.room_exists(destination) {
            return false;
        }

        character.move_to(destination.clone());
        true
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_room() {
        let mut world = World::new();

        let room = Room::new(
            String::from("room_01"),
            String::from("Entrée du château"),
            String::from("Une grande salle."),
        );

        world.add_room(room);

        assert_eq!(world.rooms.len(), 1);
    }

    #[test]
    fn test_get_room() {
        let mut world = World::new();

        let room = Room::new(
            String::from("room_01"),
            String::from("Entrée du château"),
            String::from("Une grande salle."),
        );

        world.add_room(room);

        let found = world.get_room("room_01");

        assert!(found.is_some());

        let missing = world.get_room("room_99");

        assert!(missing.is_none());
    }

    #[test]
    fn test_connected_rooms() {
        use crate::direction::Direction;

        let mut world = World::new();

        let mut room_01 = Room::new(
            String::from("room_01"),
            String::from("Entrée"),
            String::from("L'entrée du château."),
        );

        let mut room_02 = Room::new(
            String::from("room_02"),
            String::from("Bibliothèque"),
            String::from("Une pièce remplie de livres."),
        );

        room_01.add_exit(
            Direction::North,
            String::from("room_02"),
        );

        room_02.add_exit(
            Direction::South,
            String::from("room_1"),
        );

        world.add_room(room_01);
        world.add_room(room_02);

        assert_eq!(world.rooms.len(), 2);

        let room = world.get_room("room_01").unwrap();

        assert_eq!(
            room.exits.get(&Direction::North),
            Some(&String::from("room_02"))
        );
    }

    #[test]
    fn test_room_exists() {
        let mut world = World::new();

        let room = Room::new(
            String::from("room_01"),
            String::from("Entrée"),
            String::from("Une grande salle."),
        );

        world.add_room(room);

        assert!(world.room_exists("room_01"));
        assert!(!world.room_exists("room_99"));
    }

    #[test]
    fn test_connect_rooms() {
        let mut world = World::new();

        let room_01 = Room::new(
            String::from("room_01"),
            String::from("Entrée"),
            String::from("L'entrée du château."),
        );

        let room_02 = Room::new(
            String::from("room_02"),
            String::from("Bibliothèque"),
            String::from("Une pièce remplie de livres."),
        );

        world.add_room(room_01);
        world.add_room(room_02);

        assert!(world.connect_rooms(
            "room_01",
            Direction::North,
            "room_02",
        ));

        assert!(!world.connect_rooms(
            "room_01",
            Direction::South,
            "room_99",
        ));

        let room = world.get_room("room_01").unwrap();

        assert_eq!(
            room.exits.get(&Direction::North),
            Some(&String::from("room_02"))
        );

        assert!(room.exits.get(&Direction::South).is_none());
    }

    #[test]
    fn test_bidirectional_connection() {
        let mut world = World::new();

        let room_01 = Room::new(
            String::from("room_01"),
            String::from("Entrée"),
            String::from("L'entrée du château."),
        );

        let room_02 = Room::new(
            String::from("room_02"),
            String::from("Bibliothèque"),
            String::from("Une pièce remplie de livres."),
        );

        world.add_room(room_01);
        world.add_room(room_02);

        assert!(world.connect_rooms_bidirectional(
            "room_01",
            Direction::North,
            "room_02",
        ));

        let room_01 = world.get_room("room_01").unwrap();
        let room_02 = world.get_room("room_02").unwrap();

        assert_eq!(
            room_01.exits.get(&Direction::North),
            Some(&String::from("room_02"))
        );

        assert_eq!(
            room_02.exits.get(&Direction::South),
            Some(&String::from("room_01"))
        );
    }

    #[test]
    fn test_move_to_existing_room() {
        let mut world = World::new();

        let castle = Room::new(
            "castle".to_string(),
            "Le château".to_string(),
            "Un grand château".to_string(),
        );

        world.add_room(castle);

        let mut character = crate::character::Character::new(
            "player_1".to_string(),
            "Nass".to_string(),
            "forest".to_string(),
        );

        if world.room_exists("castle") {
            character.move_to("castle".to_string());
        }

        assert_eq!(character.room_id, "castle");
    }

    #[test]
    fn test_move_character() {
        let mut world = World::new();

        let mut forest = Room::new(
            "forest".to_string(),
            "La forêt".to_string(),
            "Une forêt mystérieuse".to_string(),
        );

        let castle = Room::new(
            "castle".to_string(),
            "Le château".to_string(),
            "Un grand château".to_string(),
        );

        forest.add_exit(Direction::North, "castle".to_string());

        world.add_room(forest);
        world.add_room(castle);

        let mut nass = crate::character::Character::new(
            "player_1".to_string(),
            "Nass".to_string(),
            "forest".to_string(),
        );

        assert!(world.move_character(&mut nass, &Direction::North));
        assert_eq!(nass.room_id, "castle");
    }

    #[test]
    fn test_move_character_invalid_direction() {
        let mut world = World::new();

        let forest = Room::new(
            "forest".to_string(),
            "La forêt".to_string(),
            "Une forêt mystérieuse".to_string(),
        );

        world.add_room(forest);

        let mut arthur = crate::character::Character::new(
            "player_1".to_string(),
            "Arthur".to_string(),
            "forest".to_string(),
        );

        assert!(!world.move_character(&mut arthur, &Direction::South));
        assert_eq!(arthur.room_id, "forest");
    }

    #[test]
    fn test_move_character_invalid_destination() {
        let mut world = World::new();

        let mut forest = Room::new(
            "forest".to_string(),
            "La forêt".to_string(),
            "Une forêt mystérieuse".to_string(),
        );

        forest.add_exit(Direction::North, "castle".to_string());

        world.add_room(forest);

        let mut arthur = crate::character::Character::new(
            "player_1".to_string(),
            "Arthur".to_string(),
            "forest".to_string(),
        );

        assert!(!world.move_character(&mut arthur, &Direction::North));
        assert_eq!(arthur.room_id, "forest");
    }
}