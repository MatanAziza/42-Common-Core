/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   compile.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/30 17:55:28 by maziza            #+#    #+#             */
/*   Updated: 2026/06/30 19:32:20 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <errno.h>
#include <sys/time.h>

int	unlock(t_coder *coder, int left, int right)
{
	pthread_cond_signal(&coder->data->dongles[left].cond_dongle);
	pthread_cond_signal(&coder->data->dongles[right].cond_dongle);
	pthread_mutex_unlock(&coder->data->dongles[left].mutex_dongle);
	pthread_mutex_unlock(&coder->data->dongles[right].mutex_dongle);
	return (-1 - coder->data->failure);
}

int	wait(t_coder *coder, int use, int dont_use)
{
	int	ret;

	while (!is_dongle_ready(coder->data->dongles[use], coder))
	{
		ret = pthread_cond_timedwait(&coder->data->dongles[use].cond_dongle,
				&coder->data->dongles[use].mutex_dongle, &coder->spec);
		if (ret == ETIMEDOUT || coder->data->failure)
			return (unlock(coder, use, dont_use));
	}
	if (coder->data->failure || coder->params.nb_compile == 1)
		return (unlock(coder, use, dont_use));
	update_time(coder, -1);
	printf("%s%ld %d has taken a dongle\n", ORANGE, get_time_up(coder),
		coder->id);
	return (0);
}

int	compile(t_coder *coder, int left, int right)
{
	add_burnout(coder);
	pthread_mutex_lock(&coder->data->dongles[left].mutex_dongle);
	if (wait(coder, left, right))
	{
		update_time(coder, -1);
		return (-1 - coder->data->failure);
	}
	pthread_mutex_lock(&coder->data->dongles[right].mutex_dongle);
	if (wait(coder, right, left))
	{
		return (-1 - coder->data->failure);
		update_time(coder, -1);
	}
	coder->params.nb_compile++;
	update_time(coder, 1);
	usleep(coder->params.compile_time * 1000);
	unlock(coder, left, right);
	return (1);
}
