pub struct Inventory {
    pub items: Vec<String>,
}

impl Inventory {
    pub fn new() -> Self {
        Self {
            items: Vec::new(),
        }
    }

    pub fn add_item(&mut self, item_id: String) {
        self.items.push(item_id);
    }

    pub fn remove_item(&mut self, item_id: &str) -> bool {
        if let Some(index) = self.items.iter().position(|id| id == item_id) {
            self.items.remove(index);
            return true;
        }

        false
    }

    pub fn has_item(&self, item_id: &str) -> bool {
        self.items.iter().any(|id| id == item_id)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_item() {
        let mut inventory = Inventory::new();

        inventory.add_item("sword".to_string());
        inventory.add_item("potion".to_string());

        assert_eq!(inventory.items.len(), 2);
        assert_eq!(inventory.items[0], "sword");
        assert_eq!(inventory.items[1], "potion");
    }

    #[test]
    fn test_remove_item() {
        let mut inventory = Inventory::new();

        inventory.add_item("sword".to_string());
        inventory.add_item("potion".to_string());
        inventory.add_item("key".to_string());

        assert!(inventory.remove_item("potion"));

        assert_eq!(inventory.items.len(), 2);
        assert_eq!(inventory.items[0], "sword");
        assert_eq!(inventory.items[1], "key");

        assert!(!inventory.remove_item("dragon"));
        assert_eq!(inventory.items.len(), 2);
    }

    #[test]
    fn test_has_item() {
        let mut inventory = Inventory::new();

        inventory.add_item("sword".to_string());
        inventory.add_item("potion".to_string());

        assert!(inventory.has_item("sword"));
        assert!(inventory.has_item("potion"));
        assert!(!inventory.has_item("key"));
    }
}