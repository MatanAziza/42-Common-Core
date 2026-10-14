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

int	mallocs(t_data *data, int *values)
{
	int	i;

	i = 0;
	data->dongles = malloc(sizeof(t_dongle) * values[0]);
	if (!data->dongles)
		return (1);
	while (i < values[0])
	{
		data->dongles[i].queue = malloc(sizeof(struct s_node) * 2);
		if (!data->dongles[i].queue)
			return (free_queues(data, i));
		i++;
	}
	data->coders = malloc(sizeof(t_coder) * values[0]);
	if (!data->coders)
		return (free_dongles(data));
	pthread_mutex_init(&data->mutex_data, NULL);
	return (0);
}

void	atoi_values(char **args, int **values)
{
	int	i;

	i = 0;
	while (i < 7)
	{
		(*values)[i] = atoi(args[i + 1]);
		i++;
	}
}

int	filler(char **args, t_data *data)
{
	int	*values;
	int	i;

	if (parse_check(args))
		return (1);
	values = malloc(sizeof(int) * 7);
	if (!values)
		return (1);
	atoi_values(args, &values);
	i = 0;
	if (mallocs(data, values))
		return (free_values(values));
	fill_params(values, args[8], &data->params);
	while (i < values[0])
	{
		data->coders[i] = fill_coder(data, i);
		if (fill_dongle(&data->dongles[i], values[6]))
			return (free_values(values) + destroy_mutexes(data, i));
		i++;
	}
	return (0 * free_values(values));
}
