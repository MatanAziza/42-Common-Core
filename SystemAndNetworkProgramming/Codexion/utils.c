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

void	custom_timedwait(const struct timespec *abstime)
{
	struct timespec	now;
	long			time_in_ms;
	clock_gettime(0, &now);
	if (now.tv_sec > abstime->tv_sec)
		return ;
	if (now.tv_sec == abstime->tv_sec && now.tv_nsec >= abstime->tv_nsec)
		return ;
	time_in_ms = 1000000 * (abstime->tv_sec - now.tv_sec) + (abstime->tv_nsec - now.tv_nsec) / 1000;
	usleep(time_in_ms);
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
