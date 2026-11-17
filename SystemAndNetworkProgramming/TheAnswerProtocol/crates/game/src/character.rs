pub struct Character {
    pub id: String,
    pub name: String,
    pub health: i32,
    pub room_id: String,
}

impl Character {
    pub fn new(id: String, name: String, room_id: String) -> Self {
        Self {
            id,
            name,
            health: 100,
            room_id,
        }
    }

    pub fn take_damage(&mut self, damage: i32) {
        if damage > 0 {
            self.health = (self.health - damage).max(0);
        }
    }

    pub fn is_alive(&self) -> bool {
        self.health > 0
    }

    pub fn heal(&mut self, amount: i32) {
        if amount > 0 {
            self.health = (self.health + amount).min(100);
        }
    }

    pub fn move_to(&mut self, room_id: String) {
        self.room_id = room_id;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_character() {
        let hero = Character::new(
            "player_1".to_string(),
            "Matan".to_string(),
            "castle".to_string(),
        );

        assert_eq!(hero.id, "player_1");
        assert_eq!(hero.name, "Matan");
        assert_eq!(hero.health, 100);
        assert_eq!(hero.room_id, "castle");
    }

    #[test]
    fn test_take_damage() {
        let mut hero = Character::new(
            "player_1".to_string(),
            "Matan".to_string(),
            "castle".to_string(),
        );

        hero.take_damage(30);
        assert_eq!(hero.health, 70);

        hero.take_damage(100);
        assert_eq!(hero.health, 0);
    }

    #[test]
    fn test_is_alive() {
        let mut hero = Character::new(
            "player_1".to_string(),
            "Matan".to_string(),
            "castle".to_string(),
        );

        assert!(hero.is_alive());

        hero.take_damage(100);

        assert!(!hero.is_alive());
    }

    #[test]
    fn test_heal() {
        let mut hero = Character::new(
            "player_1".to_string(),
            "Matan".to_string(),
            "castle".to_string(),
        );

        hero.take_damage(40);
        assert_eq!(hero.health, 60);

        hero.heal(30);
        assert_eq!(hero.health, 90);

        hero.heal(50);
        assert_eq!(hero.health, 100);

        hero.heal(-20);
        assert_eq!(hero.health, 100);
    }

    #[test]
    fn test_move_to() {
        let mut character = Character::new(
            "player_1".to_string(),
            "Matan".to_string(),
            "forest".to_string(),
        );

        character.move_to("castle".to_string());

        assert_eq!(character.room_id, "castle");
    }
}