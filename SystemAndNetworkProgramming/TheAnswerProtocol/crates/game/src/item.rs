pub struct Item {
    pub id: String,
    pub name: String,
    pub description: String,
}

impl Item {
    pub fn new(id: String, name: String, description: String) -> Self {
        Self {
            id,
            name,
            description,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_item() {
        let sword = Item::new(
            "item_1".to_string(),
            "Sword".to_string(),
            "Sword argent".to_string(),
        );

        assert_eq!(sword.id, "item_1");
        assert_eq!(sword.name, "Sword");
        assert_eq!(sword.description, "Sword argent");
    }
}