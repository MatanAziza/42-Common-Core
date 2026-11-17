use crate::character::Character;

pub struct Npc {
    pub character: Character,
    pub role: String,
}

impl Npc {
    pub fn new(character: Character, role: String) -> Self {
        Self {
            character,
            role,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_npc() {
        let character = Character::new(
            "npc_1".to_string(),
            "Gandalf".to_string(),
            "castle".to_string(),
        );

        let npc = Npc::new(
            character,
            "quest_giver".to_string(),
        );

        assert_eq!(npc.character.name, "Gandalf");
        assert_eq!(npc.character.health, 100);
        assert_eq!(npc.role, "quest_giver");
    }
}