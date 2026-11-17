use game::direction::Direction;
use crate::command::{Command, MessageScope};
use crate::error::{ServerError, CommandError};

// fn packet_to_string(packet: Vec<u8>) -> Result<String, String> {
// 	String::from_utf8(packet)
// 		.map_err(|_| "ERR 101 INVALID_COMMAND".to_string())
// }

fn parse_simple_command(str_packet: &str) -> Option<Command> {
	let mut words = str_packet.split_whitespace();

	match words.next() {
		Some("LOOK") => Some(Command::Look),
		Some("QUIT") => Some(Command::Quit),
		Some("WHO") => Some(Command::Who),
		Some("INVENTORY") => Some(Command::Inventory),
		Some("STATUS") => Some(Command::Status),
		Some("QUESTS") => Some(Command::Quests),
		_ => None,
	}
}

fn parse_move(str_packet: &str) -> Option<Command> {
	let mut words = str_packet.split_whitespace();

	match words.next() {
		Some("MOVE") => {
			match words.next() {
				Some("North") => Some(Command::Move {direction: Direction::North}),
				Some("South") => Some(Command::Move {direction: Direction::South}),
				Some("East") => Some(Command::Move {direction: Direction::East}),
				Some("West") => Some(Command::Move {direction: Direction::West}),
				Some("Up") => Some(Command::Move {direction: Direction::Up}),
				Some("Down") => Some(Command::Move {direction: Direction::Down}),
				_ => None,
			}
		},
		_ => None,
	}
}

fn parse_string_argument(str_packet: &str) -> Option<Command> {
	let mut words = str_packet.split_whitespace();

	match words.next() {
		Some("TAKE") => Some(Command::Take {item: words.next()?.to_string()}),
		Some("DROP") => Some(Command::Drop {item: words.next()?.to_string()}),
		Some("TALK") => Some(Command::Talk {name: words.next()?.to_string()}),
		Some("ATTACK") => Some(Command::Attack {name: words.next()?.to_string()}),
		Some("QUEST") => Some(Command::Quest {name: words.next()?.to_string()}),
		_ => None,
	}
}

fn parse_group_command(str_packet: &str, count: usize) -> Option<Command> {
	let mut words = str_packet.split_whitespace();

	match (words.next(), words.next()) {
		(Some("GROUP"), Some("CREATE")) if count == 3 => Some(Command::GroupCreate {name: words.next()?.to_string()}),
		(Some("GROUP"), Some("INVITE")) if count == 4 => {
			let group_name = words.next()?.to_string();
			let player_name = words.next()?.to_string();
				
			Some(Command::GroupInvit {group_name, player_name})},
		(Some("GROUP"), Some("JOIN")) if count == 3  => Some(Command::GroupJoin {name: words.next()?.to_string()}),
		(Some("GROUP"), Some("LEAVE")) if count == 3 => Some(Command::GroupLeave {name: words.next()?.to_string()}),
		_ => None,
	}
}

fn parse_chat(str_packet: &str, count: usize) -> Option<Command> {
	let mut words = str_packet.split_whitespace();

	match words.next() {
		Some("CHAT") => {
			match words.next() {
				Some("GLOBAL") => Some(Command::Chat {scope: MessageScope::Global, message: words.collect::<Vec<&str>>().join(" ")}),
				Some("ROOM") => Some(Command::Chat {scope: MessageScope::Room, message: words.collect::<Vec<&str>>().join(" ")}),
				Some("GROUP") if count > 3 => Some(Command::Chat {scope: MessageScope::Group {name: words.next()?.to_string()}, message: words.collect::<Vec<&str>>().join(" ")}),
				_ => None,
			}
		},
		_ => None,
	}
}

fn parse_command(str_packet: String) -> Result<Command, ServerError> {
	// il manque le parsing de help !!!!
	let str_packet = str_packet.strip_suffix("\n").ok_or(ServerError::Protocol(CommandError::InvalidCommand))?;

	let count = str_packet.split_whitespace().count();

	match count {
		0 => Err(ServerError::Protocol(CommandError::InvalidCommand)),
		1 => parse_simple_command(str_packet)
			.ok_or_else(|| ServerError::Protocol(CommandError::InvalidCommand)),
		2 => parse_move(str_packet)
			.or_else(|| parse_string_argument(&str_packet))
			.ok_or_else(|| ServerError::Protocol(CommandError::InvalidCommand)),
		_ => parse_group_command(str_packet, count)
			.or_else(|| parse_chat(str_packet, count))
			.ok_or_else(|| ServerError::Protocol(CommandError::InvalidCommand))
	}
}

fn parse_connect(str_packet: String) -> Result<Command, ServerError> {
	let str_packet = str_packet.strip_suffix("\r\n").ok_or(ServerError::Protocol(CommandError::InvalidCommand))?;

	let count = str_packet.split_whitespace().count();


	match count {
		2 => {
			let mut words = str_packet.split_whitespace();

			match words.next() {
				Some("CONNECT") => Ok(Command::Connect {name: words.next().unwrap().to_string()}),
				_ => Err(ServerError::Protocol(CommandError::InvalidCommand)),
			}
		}
		_ => Err(ServerError::Protocol(CommandError::InvalidCommand)),
	}
}

pub fn parse_packet(packet: String) -> Result<Command, ServerError> {
	// attention quand on travaillera en donnee brut packet sera type en Vec<u8>
	// let str_packet = packet_to_string(packet)?;

	// condition pour verifier si premiere connection 
	// sinon parse_command classique 
	if packet.contains("CONNECT") {
		parse_connect(packet)
	} else {
		parse_command(packet)
	}
}