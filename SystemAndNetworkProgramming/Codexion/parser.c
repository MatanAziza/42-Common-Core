/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parser.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/12 16:18:59 by maziza            #+#    #+#             */
/*   Updated: 2026/06/22 17:36:40 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <pthread.h>

int	check_arg_int(char *arg)
{
	int	i;

	i = 0;
	while (arg[i])
	{
		if ('0' > arg[i] || arg[i] > '9')
			return (1);
		i++;
	}
	return (0);
}

void	fill_coder(t_coder *coder, int id, int *values)
{
	coder->id = id;
	coder->state = WAITING;
	coder->burnout_time = values[0];
	coder->compile_time = values[1];
	coder->debug_time = values[2];
	coder->refactor_time = values[3];
	coder->max_compile = values[4];
	coder->nb_compile = 0;
}

void	fill_dongle(t_dongle *dongle, int cd)
{
	dongle->to_who = -1;
	dongle->cooldown = cd;
	dongle->last_use = 0;
	pthread_mutex_init(&dongle->mutex_dongle, NULL);
	pthread_cond_init(&dongle->cond_dongle, NULL);
}


int	parse_check(char **argv)
{
	int	i;

	i = 1;
	while (i < 8)
	{
		if (check_arg_int(argv[i]))
			return (1);
		i++;
	}
	if (strcmp("fifo", argv[8]) && strcmp("edf", argv[8]))
		return (1);
	return (0);
}

void	filler(char **args, t_data *data)
{
	int	*atoied;
	int	i;

	i = 1;
	atoied = malloc(sizeof(int) * 7);
	while (i < 8)
	{
		atoied[i - 1] = atoi(args[i]);
		i++;
	}
	i = 0;
	data->dongles = malloc(sizeof(struct s_dongle) * atoied[0]);
	data->coders = malloc(sizeof(struct s_coder) * atoied[0]);
	data->queues = malloc(sizeof(struct s_queue) * atoied[0]);
	while (i < atoied[0])
	{
		fill_dongle(&data->dongles[i], atoied[6]);
		fill_coder(&data->coders[i], i, atoied);
		data->queues->head = malloc(sizeof(struct s_node));
		data->coders[i].dongles = &data->dongles[0];
		data->coders[i].queues = &data->queues[0];
		i++;
	}
	free(atoied);
}
