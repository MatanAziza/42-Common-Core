use crate::error::{ServerError, handle_error};
use crate::parser::parse_packet;
use crate::command::handle_command;

pub fn create_response(packet: String) -> Result<String, ServerError> {
	match parse_packet(packet) {
		Ok(command) => match handle_command(command) {
			Ok(success) => { 
			let answer = success.to_string()
				.map_err(ServerError::Serialization)?;
			Ok(answer)
			},
			Err(error) => handle_error(error),
		},
		Err(error) => handle_error(error),
	}
}