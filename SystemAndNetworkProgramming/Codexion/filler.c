/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   filler.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/13 13:55:11 by maziza            #+#    #+#             */
/*   Updated: 2026/10/13 13:57:48 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <pthread.h>

int	free_values(int *values)
{
	free(values);
	return (1);
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

int	fill_dongle(t_dongle *dongle, int cd)
{
	dongle->to_who = -1;
	dongle->cooldown = cd;
	dongle->queue_index = 0;
	if (pthread_mutex_init(&dongle->mutex_dongle, NULL))
		return (1);
	return (0);
}

t_coder	fill_coder(t_data *data, int id)
{
	t_coder	coder;

	coder.id = id;
	coder.params = data->params;
	coder.data = data;
	return (coder);
}
