/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parser.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/12 16:18:59 by maziza            #+#    #+#             */
/*   Updated: 2026/06/12 18:30:04 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"

int	check_arg_int(char *arg){
	int	i;

	i = 0;
	while (arg[i]){
		if ('0' > arg[i] || arg[i] > '9')
			return (1);
	}
	return (0);
}

void	fill_coder(t_coder coder, int id, int *values){
	coder.id = id;
	coder.state = WAITING;
	coder.burnout_time = values[0];
	coder.compile_time = values[1];
	coder.debug_time = values[2];
	coder.refactor_time = values[3];
	coder.nb_compile = values[4];
}

void	fill_dongle(t_dongle dongle, int id, int cd){

}

int	parser(char **args, t_data	*p_data){
	t_data	data;
	int		*atoied;
	int		i;

	i = 0;
	atoied = malloc(sizeof(int) * 7);
	data = *p_data;
	while (i < 7){
		if (check_arg_int(args[i]))
			return (free_atoied(atoied));
		atoied[i] = atoi(args[i]);
		i++;
	}
	if (!strcmp("fifo", args[7]) || !strcmp("edf", args[7]))
		return (free_atoied(atoied));
	i = 0;
	while (i < atoied[0]){
		fill_dongle(data.dongles[i], i, atoied[6]);
		i++;
	}
	return (0);
}
