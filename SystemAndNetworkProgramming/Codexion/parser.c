/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parser.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/12 16:18:59 by maziza            #+#    #+#             */
/*   Updated: 2026/06/25 14:22:41 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <pthread.h>

int	parse_check(char **argv)
{
	int	i;

	i = 1;
	while (i < 8)
	{
		if (check_arg_int(argv[i]))
			return (1 + 0
				* printf("Parameter is supposed to be an int value.\n"));
		i++;
	}
	if (strcmp("fifo", argv[8]) && strcmp("edf", argv[8]))
		return (1 + 0 * printf("Wrong scheduler format.\n"));
	return (0);
}

void	fill_params(int *values, char *mode, t_params *params)
{
	params->nb_threads = values[0];
	params->burnout_time = values[1];
	params->compile_time = values[2];
	params->debug_time = values[3];
	params->refactor_time = values[4];
	params->max_compile = values[5];
	params->dongle_cooldown = values[6];
	params->mode = mode;
	params->nb_compile = 0;
}

void	fill_dongle(t_dongle *dongle, int cd)
{
	dongle->to_who = -1;
	dongle->cooldown = cd;
	pthread_mutex_init(&dongle->mutex_dongle, NULL);
	pthread_cond_init(&dongle->cond_dongle, NULL);
}

int	mallocs(t_data *data, int *values)
{
	data->dongles = malloc(sizeof(t_dongle) * values[0]);
	if (!data->dongles)
		return (1);
	data->coders = malloc(sizeof(t_coder) * values[0]);
	if (!data->coders)
		return (free_dongles(data));
	return (0);
}

int	filler(char **args, t_data *data)
{
	int	*values;
	int	i;

	i = 0;
	values = malloc(sizeof(int) * 7);
	if (!values)
		return (1);
	if (parse_check(args))
		return (free_values(values));
	while (i < 7)
	{
		values[i] = atoi(args[i + 1]);
		i++;
	}
	i = 0;
	if (mallocs(data, values))
		return (free_values(values));
	fill_params(values, args[8], &data->params);
	while (i < values[0])
	{
		data->coders[i] = fill_coder(data, i);
		fill_dongle(&data->dongles[i++], values[6]);
	}
	free(values);
	return (0);
}
