/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/25 13:46:25 by maziza            #+#    #+#             */
/*   Updated: 2026/06/25 14:22:46 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include <time.h>

void	swap(int *a, int *b, int cond)
{
	int	swap;

	if (!cond)
		return ;
	swap = *b;
	*b = *a;
	*a = swap;
}
/*
	long			time_in_ms;
	if (now.tv_sec > abstime->tv_sec)
		return (1);
	if (now.tv_sec == abstime->tv_sec && now.tv_nsec >= abstime->tv_nsec)
		return (1);
	time_in_ms = 1000000 * (abstime->tv_sec - now.tv_sec) + (abstime->tv_nsec
			- now.tv_nsec) / 1000;
	usleep(time_in_ms);
*/

int	custom_timedwait(const struct timespec *abstime, t_coder *coder)
{
	struct timespec	now;

	clock_gettime(0, &now);
	while (1)
	{
		clock_gettime(0, &now);
		if (now.tv_sec > abstime->tv_sec)
			break ;
		if (now.tv_sec == abstime->tv_sec && now.tv_nsec >= abstime->tv_nsec)
			break ;
		if (has_burnt_out(coder))
			return (1);
		usleep(1);
	}
	return (0);
}

int	custom_sleep(t_coder *coder, long cooldown)
{
	struct timespec	timer;
	struct timespec	ref;

	clock_gettime(0, &timer);
	ref = timer;
	add_time(&ref, cooldown);
	while (1)
	{
		clock_gettime(0, &timer);
		if (timer.tv_sec > ref.tv_sec)
			break ;
		if (timer.tv_sec == ref.tv_sec && timer.tv_nsec >= ref.tv_nsec)
			break ;
		if (has_burnt_out(coder))
			return (1);
		usleep(1);
	}
	return (0);
}

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
