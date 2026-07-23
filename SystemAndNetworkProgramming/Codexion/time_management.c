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

#include "header.h"
#include "structs.h"
#include <stdio.h>
#include <sys/time.h>
#include <time.h>

void	start_time(t_data *data)
{
	gettimeofday(&data->time, NULL);
	clock_gettime(0, &data->spec);
	data->start = 1;
}

void	update_time(t_coder *coder, int result)
{
	gettimeofday(&coder->time, NULL);
	if (result == 4 || result == 1)
		clock_gettime(0, &coder->data->spec);
	if (!coder->data->failure && result > 0)
	{
		if (result == 1)
			printf("%s%ld %d compiled\n", VIOLET, get_time_up(coder),
				coder->id);
		else if (result == 2)
			printf("%s%ld %d debugged\n", BLUE, get_time_up(coder), coder->id);
		else if (result == 3)
			printf("%s%ld %d refactored\n", YELLOW, get_time_up(coder),
				coder->id);
	}
}

void	add_burnout(t_coder *coder)
{
	long	burnout_ms;

	burnout_ms = (coder->params.burnout_time % 1000);
	coder->spec.tv_nsec += (burnout_ms * 1000000);
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

// long	get_dongle_cd(t_dongle *dongle)
// {
// 	return (0);
// }
