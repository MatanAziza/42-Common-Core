pub struct Group {
    pub id: String,
    pub name: String,
    pub members: Vec<String>,
}

impl Group {
    pub fn new(id: String, name: String) -> Self {
        Self {
            id,
            name,
            members: Vec::new(),
        }
    }

    pub fn add_member(&mut self, player_id: String) {
        self.members.push(player_id);
    }

    pub fn remove_member(&mut self, player_id: &str) -> bool {
        if let Some(index) = self.members.iter().position(|id| id == player_id) {
            self.members.remove(index);
            return true;
        }

        false
    }

    pub fn has_member(&self, player_id: &str) -> bool {
        self.members.iter().any(|id| id == player_id)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_member() {
        let mut group = Group::new(
            "group_1".to_string(),
            "Les Aventuriers".to_string(),
        );

        group.add_member("Anna".to_string());
        group.add_member("Matan".to_string());

        assert_eq!(group.members.len(), 2);
        assert_eq!(group.members[0], "Anna");
        assert_eq!(group.members[1], "Matan");
    }

    #[test]
    fn test_remove_member() {
        let mut group = Group::new(
            "group_1".to_string(),
            "Les Aventuriers".to_string(),
        );

        group.add_member("Anna".to_string());
        group.add_member("Matan".to_string());
        group.add_member("Samira".to_string());

        assert!(group.remove_member("Matan"));

        assert_eq!(group.members.len(), 2);
        assert_eq!(group.members[0], "Anna");
        assert_eq!(group.members[1], "Samira");

        assert!(!group.remove_member("Nass"));
        assert_eq!(group.members.len(), 2);
    }

    #[test]
    fn test_has_member() {
        let mut group = Group::new(
            "group_1".to_string(),
            "Les Aventuriers".to_string(),
        );

        group.add_member("Anna".to_string());
        group.add_member("Matan".to_string());

        assert!(group.has_member("Anna"));
        assert!(group.has_member("Matan"));
        assert!(!group.has_member("Nass"));
    }
}