pub struct Quest {
    pub id: String,
    pub title: String,
    pub description: String,
}

impl Quest {
    pub fn new(id: String, title: String, description: String) -> Self {
        Self {
            id,
            title,
            description,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_quest() {
        let quest = Quest::new(
            "quest_1".to_string(),
            "La clé perdue".to_string(),
            "Retrouver la clé du château".to_string(),
        );

        assert_eq!(quest.id, "quest_1");
        assert_eq!(quest.title, "La clé perdue");
        assert_eq!(quest.description, "Retrouver la clé du château");
    }
}