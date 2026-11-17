use crate::character::Character;
use crate::inventory::Inventory;

pub struct Player {
    pub character: Character,
    pub connected: bool,
    pub inventory: Inventory,
}

impl Player {
    pub fn new(character: Character) -> Self {
        Self {
            character,
            connected: true,
            inventory: Inventory::new(),
        }
    }

    pub fn disconnect(&mut self) {
        self.connected = false;
    }

    pub fn reconnect(&mut self) {
        self.connected = true;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_disconnect() {
        let character = Character::new(
            "player_1".to_string(),
            "Anna".to_string(),
            "castle".to_string(),
        );

        let mut player = Player::new(character);

        assert!(player.connected);

        player.disconnect();

        assert!(!player.connected);
    }

    #[test]
    fn test_reconnect() {
        let character = Character::new(
            "player_1".to_string(),
            "Anna".to_string(),
            "castle".to_string(),
        );

        let mut player = Player::new(character);

        player.disconnect();
        assert!(!player.connected);

        player.reconnect();
        assert!(player.connected);
    }

    #[test]
    fn test_player_inventory() {
        let character = Character::new(
            "player_1".to_string(),
            "Anna".to_string(),
            "castle".to_string(),
        );

        let mut player = Player::new(character);

        assert_eq!(player.inventory.items.len(), 0);

        player.inventory.add_item("sword".to_string());

        assert_eq!(player.inventory.items.len(), 1);
        assert!(player.inventory.has_item("sword"));
    }
}