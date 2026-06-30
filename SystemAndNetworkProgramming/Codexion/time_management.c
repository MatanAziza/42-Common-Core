/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   time_management.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/27 14:04:20 by maziza            #+#    #+#             */
/*   Updated: 2026/06/27 14:04:30 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "structs.h"
#include <stdio.h>
#include <sys/time.h>

void	start_time(t_data *data)
{
	gettimeofday(&data->time, NULL);
	data->spec.tv_nsec = data->time.tv_usec * 1000;
	data->spec.tv_sec = data->time.tv_sec;
	data->start = 1;
}

void	update_time(t_coder *coder)
{
	gettimeofday(&coder->time, NULL);
	coder->spec.tv_nsec = coder->time.tv_usec * 1000;
	coder->spec.tv_sec = coder->time.tv_sec;
}

void	add_burnout(t_coder *coder)
{
	int	burnout_ms;

	burnout_ms = (coder->params.burnout_time % 1000);
	coder->spec.tv_nsec += burnout_ms * 1000000;
	coder->spec.tv_sec += coder->params.burnout_time / 1000;
	coder->spec.tv_nsec %= 1000000000;
}

long	get_time_up(t_coder *coder)
{
	long	time_elapsed;

	time_elapsed = coder->time.tv_sec * 1000 - coder->data->time.tv_sec * 1000;
	time_elapsed -= coder->data->time.tv_usec / 1000;
	time_elapsed += coder->time.tv_usec / 1000;
	return (time_elapsed);
}

struct timespec	time_elapsed(struct timespec smaller, struct timespec bigger)
{
	struct timespec	result;

	result.tv_sec = bigger.tv_sec - smaller.tv_sec;
	if (bigger.tv_nsec < smaller.tv_nsec)
	{
		result.tv_nsec = 1000000000 - smaller.tv_nsec + bigger.tv_nsec;
		result.tv_sec--;
	}
	else
		result.tv_nsec = bigger.tv_nsec - smaller.tv_nsec;
	return (result);
}
