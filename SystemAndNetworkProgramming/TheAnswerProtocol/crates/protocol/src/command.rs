use game::direction::Direction;
use crate::action::*;
use crate::error::ServerError;
use crate::success::Success;

#[derive(Debug, PartialEq)]
pub enum Command {
	Connect {name: String}, // CONNECT player_name ==> rep[OK, ERR 201 NAME_IN_USE, ERR 900 CONNECTION FAILED]
	Look, // LOOK ==> rep[OK current room state as JSON]
	Move {direction: Direction}, // MOVE dirrection ==> rep[OK room=new_room, ERR 301 NO_EXIT]
	Quit, // QUIT ==> rep[OK bye]
	Chat {scope: MessageScope, message: String}, // CHAT SCOPE "message" ==> rep[OK, ERR 401 NOT_IN_GROUP, ERR 403 GROUP_NOT_FOUND]
	Who, // WHO ==> rep[OK players=nb_players]
	GroupCreate {name: String}, // GROUP CREATE group_name ==> rep[OK group=group_name, ERR 201 NAME_IN_USE]
	GroupInvit {group_name: String, player_name: String}, // GROUP INVITE group_name player_name ==> rep[OK, ERR 401 NOT_IN_GROUP, ERR 402 ALREADY_IN_GROUP, ERR 403 GROUP_NOT_FOUND, ERR 202 NAME_NOT_FOUND]
	GroupJoin {name: String}, // GROUP JOIN group_name ==> rep[OK group=group_name, ERR 403 GROUP_NOT_FOUND, ERR 402 ALREADY_IN_GROUP]
	GroupLeave {name: String}, // GROUP LEAVE group_name ==> rep[OK, ERR 403 GROUP_NOT_FOUND]
	Take {item: String}, // TAKE item_name ==> rep[OK taken=item_name, ERR 404 ITEM_NOT_FOUND]
	Drop {item: String}, // DROP item_name ==> rep[OK dropped=item_name, ERR 404 ITEM_NOT_IN_INVENTORY]
	Inventory,  // INVENTORY ==> rep[OK [current items as JSON array]]
	Talk {name: String}, // TALK ncp_name ==> rep[OK "ncp_message", ERR 404 NPC_NOT_FOUND]
	Attack {name: String}, // ATTACK ncp_name ==> rep[OK combat_status_as_JSON, ERR 404 NPC_NOT_FOUND, ERR 405 NPC_NOT_HOSTILE]
	Status, // STATUS ==>  rep[OK {"hp": , "max_hp": , "status": ""}]
	// ATTENTION D'AUTRES COMMANDES A IMPLEMENTER POUR LES COMBATS
	// DEFEND
	// FLEE
	// USE_ITEM
	Quest {name: String}, // QUEST ncp_name ==> rep[OK quest_data_as_json, ERR 404 NPC_NOT_FOUND, ERR 406 NO_QUEST_AVAILABLE]
	Quests, // QUESTS ==> rep[OK list_all_player_quest_data_as_JSON_array]
	// ATTENTION D'AUTRES COMMANDES A IMPLEMENTER POUR LES QUESTS
	// COMPLETE_QUEST
	// ABANDON_QUEST
	// Help , // HELP optional_command_name ==> rep[OK rules, ERR 101 COMMAND_NOT_FOUND]

}

#[derive(Debug, PartialEq)]
pub enum MessageScope {
	Global,
	Room,
	Group {name: String},
}

pub fn handle_command(command: Command) -> Result<Success, ServerError> {
	match command {
		Command::Connect {name} => connect_player(name),
		Command::Look => look(),
		Command::Move {direction} => new_direction(direction),
		Command::Quit => quit(),
		Command::Chat {scope, message} => send_message(scope, message), // avoir pour le ownership ou la ref
		Command::Who => who(),
		Command::GroupCreate {name} => create_group(name),
		Command::GroupInvit {group_name, player_name} => group_invit(&group_name, &player_name),
		Command::GroupJoin {name} => group_join(&name),
		Command::GroupLeave {name} => group_leave(&name),
		Command::Take {item} => take_item(&item),
		Command::Drop {item} => drop_item(&item),
		Command::Inventory => inventory(),
		Command::Talk {name} => talk_ncp(&name),
		Command::Attack {name} => attack_ncp(&name),
		// DEFEND
		// FLEE
		// USE_ITEM
		Command::Status => status_player(),
		Command::Quest {name} => ask_for_quest(&name),
		// ABANDON_QUEST
		// COMPLETE_QUEST
		Command::Quests => inventory_quests(),
		// Command::Help => help(),
	}
}


// fn encode_answer(answer: &str) -> ?? {}
// ajoute le caractere de fin de message et encode en UTF-8 
// implementer les methodes qui renvoie les str pour faire le paquets en UTF-8


// #[cfg(test)]
// mod tests {
// 	use super::*;


// 	// #[test]
// 	// fn you_can_decoder() {
// 	// 	let valid_packet: Vec<u8> = vec![0xE4, 0xBD, 0xA0,
//     // 0xE5, 0xA5, 0xBD];
// 	// 	let invalid_packet: Vec<u8> = vec![0xE4, 0xBD];

// 	// 	assert_eq!(packet_to_string(valid_packet), Ok("你好".to_string()));
// 	// 	assert_eq!(packet_to_string(invalid_packet), Err("ERR 101 INVALID_COMMAND".to_string()));
// 	// }

// 	#[test]
// 	fn you_can_parse_simple_command() {
// 		assert_eq!(
// 			parse_simple_command("LOOK"), 
// 			Some(Command::Look));
// 		assert_eq!(
// 			parse_simple_command("QUIT"), 
// 			Some(Command::Quit));
// 		assert_eq!(
// 			parse_simple_command("WHO"), 
// 			Some(Command::Who));
// 		assert_eq!(
// 			parse_simple_command("INVENTORY"), 
// 			Some(Command::Inventory));
// 		assert_eq!(
// 			parse_simple_command("STATUS"), 
// 			Some(Command::Status));
// 		assert_eq!(
// 			parse_simple_command("QUESTS"), 
// 			Some(Command::Quests));
// 		assert_eq!(
// 			parse_simple_command("bonjour"), 
// 			None);
// 	}

// 	#[test]
// 	fn you_can_parse_move() {
// 		assert_eq!(
// 			parse_move("MOVE North"), 
// 			Some(Command::Move {direction: Direction::North}));
// 		assert_eq!(
// 			parse_move("MOVE Sud"), 
// 			Some(Command::Move {direction: Direction::Sud}));
// 		assert_eq!(
// 			parse_move("MOVE East"), 
// 			Some(Command::Move {direction: Direction::East}));
// 		assert_eq!(
// 			parse_move("MOVE West"), 
// 			Some(Command::Move {direction: Direction::West}));
// 		assert_eq!(
// 			parse_move("VOY North"), 
// 			None);
// 		assert_eq!(
// 			parse_move("MOVE Marseille"), 
// 			None);
// 	}

// 	#[test]
// 	fn you_can_parse_string_argument() {
// 		assert_eq!(
// 			parse_string_argument("TAKE pizza"), 
// 			Some(Command::Take {item: "pizza".to_string()}));
// 		assert_eq!(
// 			parse_string_argument("DROP pizza"), 
// 			Some(Command::Drop {item: "pizza".to_string()}));
// 		assert_eq!(
// 			parse_string_argument("TALK macron"), 
// 			Some(Command::Talk {name: "macron".to_string()}));
// 		assert_eq!(
// 			parse_string_argument("ATTACK macron"), 
// 			Some(Command::Attack {name: "macron".to_string()}));
// 		assert_eq!(
// 			parse_string_argument("QUEST marx"), 
// 			Some(Command::Quest {name: "marx".to_string()}));
// 		assert_eq!(
// 			parse_string_argument("TEST wifi"), 
// 			None);
// 	}

// 	#[test]
// 	fn you_can_parse_group_command() {
// 		assert_eq!(
// 			parse_group_command("CREATE GROUP test", 3),
// 			Some(Command::GroupCreate {
// 				name: "test".to_string()}));
// 		assert_eq!(
// 			parse_group_command("GROUP INVITE test Alice", 4),
// 			Some(Command::GroupInvit {
// 				group_name: "test".to_string(),
// 				player_name: "Alice".to_string()}));
// 		assert_eq!(
// 			parse_group_command("GROUP JOIN test", 3),
// 			Some(Command::GroupJoin {
// 				name: "test".to_string()}));
// 		assert_eq!(
// 			parse_group_command("GROUP LEAVE test", 3),
// 			Some(Command::GroupLeave {
// 				name: "test".to_string()}));
// 		assert_eq!(
// 			parse_group_command("GROUP DELETE test", 3), 
// 			None);
// 		assert_eq!(
// 			parse_group_command("CREATE GROUP test", 6),
// 			None);
// 	}

// 	#[test]
// 	fn you_can_parse_chat() {
// 		assert_eq!(
// 			parse_chat("CHAT GLOBAL Hello everyone", 4),
// 			Some(Command::Chat {
// 				scope: MessageScope::Global,
// 				message: "Hello everyone".to_string()}));
// 		assert_eq!(
// 			parse_chat("CHAT ROOM Hello there", 4),
// 			Some(Command::Chat {
// 				scope: MessageScope::Room,
// 				message: "Hello there".to_string()}));
// 		assert_eq!(
// 			parse_chat("CHAT GROUP warriors Hello everyone", 5),
// 			Some(Command::Chat {
// 				scope: MessageScope::Group {
// 					name: "warriors".to_string()
// 				},
// 				message: "Hello everyone".to_string()}));
// 		assert_eq!(
// 			parse_chat("SAY GLOBAL Hello", 3), 
// 			None);
// 		assert_eq!(
// 			parse_chat("CHAT PRIVATE Hello", 3), 
// 			None);
// 		assert_eq!(
// 			parse_chat("CHAT GROUP warriors", 3), 
// 			None);
// 	}

// 	#[test]
// 	fn you_can_parse_command() {
// 		assert!(matches!(
// 			parse_command(" \n".to_string()),
// 			Err(ServerError::Protocol(CommandError::InvalidCommand))));
// 		assert!(matches!(
// 			parse_command("\n".to_string()),
// 			Err(ServerError::Protocol(CommandError::InvalidCommand))));
// 		assert!(matches!(
// 			parse_command("QUIT".to_string()),
// 			Err(ServerError::Protocol(CommandError::InvalidCommand))));
// 		assert!(matches!(
// 			parse_command("QUIT\n".to_string()),
// 			Ok(Command::Quit)));
// 		assert!(matches!(
// 			parse_command("CHAT\n".to_string()),
// 			Err(ServerError::Protocol(CommandError::InvalidCommand))));
// 		assert!(matches!(
// 			parse_command("MOVE North\n".to_string()),
// 			Ok(Command::Move {direction: Direction::North})));
// 		assert!(matches!(
// 			parse_command("CHAT GLOBAL coucou\n".to_string()),
// 			Ok(Command::Chat {
// 				scope: MessageScope::Global,
// 				message})
// 			if message == "coucou".to_string()));
// 		assert!(matches!(
// 			parse_command("CREATE GROUP banana\n".to_string()),
// 			Ok(Command::GroupCreate {
// 				name})
// 			if name == "banana".to_string()));
// 	}

// 	#[test]
// 	fn you_can_parse_connect() {
// 		assert!(matches!(
// 			parse_connect("CONNECT".to_string()),
// 			Err(ServerError::Protocol(CommandError::InvalidCommand))
// 		));
// 		assert!(matches!(
// 			parse_connect("CONNECT \r\n".to_string()),
// 			Err(ServerError::Protocol(CommandError::InvalidCommand))
// 		));
// 		assert!(matches!(
// 			parse_connect("CONNECT anana\r\n".to_string()),
// 			Ok(Command::Connect {name})
// 			if name == "anana".to_string()
// 		));
// 		// trop pratique : 
// 		// let result = parse_connect("CONNECT anana\r\n".to_string());
// 		// dbg!(&result);
// 	}

// 	// #[test]
// 	// fn you_can_parse_packet() {
// 	// 	todo!();
// 	// }

// 	// #[test]
// 	// fn you_can_handle_command(){
// 	// 	todo!();
// 	// }

// 	// #[test]
// 	// fn you_can_create_response() {
// 	// 	todo!();
// 	// }
// }