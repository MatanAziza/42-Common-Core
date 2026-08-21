/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   compile.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/30 17:55:28 by maziza            #+#    #+#             */
/*   Updated: 2026/08/14 14:56:45 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <errno.h>
#include <pthread.h>
#include <sys/time.h>
#include <time.h>

int	unlock(t_coder *coder, int left, int right)
{
	update_time(coder, 0);
	// To do: replace next 2 lines with queue to_who
	coder->data->dongles[left].to_who = -1;
	coder->data->dongles[right].to_who = -1;
	clock_gettime(0, &coder->data->dongles[left].ts);
	clock_gettime(0, &coder->data->dongles[right].ts);
	add_time(&coder->data->dongles[left].ts, coder->params.dongle_cooldown);
	add_time(&coder->data->dongles[right].ts, coder->params.dongle_cooldown);
	pthread_cond_signal(&coder->data->dongles[left].cond_dongle);
	pthread_cond_signal(&coder->data->dongles[right].cond_dongle);
	pthread_mutex_unlock(&coder->data->dongles[left].mutex_dongle);
	pthread_mutex_unlock(&coder->data->dongles[right].mutex_dongle);
	return (1);
}

int	has_burnt_out(t_coder *coder)
{
	struct timespec	ts;

	clock_gettime(0, &ts);
	// printf("%ld.%ld %d actual\n", ts.tv_sec%100, ts.tv_nsec/1000000, coder->id);
	// printf("%ld.%ld %d burnout\n", coder->spec.tv_sec%100, coder->spec.tv_nsec/1000000, coder->id);
	if (coder->spec.tv_sec > ts.tv_sec)
		return (0);
	else if (coder->spec.tv_sec == ts.tv_sec){
		if (coder->spec.tv_nsec >= ts.tv_nsec)
			return (0);
	return (1);
	}
	return (1);
}

int	wait(t_coder *coder, int left, int right)
{
	while (1)
	{
		if (is_dongle_ready(&coder->data->dongles[left], coder)
			&& is_dongle_ready(&coder->data->dongles[right], coder))
			break ;
		pthread_cond_timedwait(&coder->data->dongles[left].cond_dongle,
			&coder->data->dongles[left].mutex_dongle,
			&coder->data->dongles[left].ts);
		pthread_cond_timedwait(&coder->data->dongles[right].cond_dongle,
			&coder->data->dongles[right].mutex_dongle,
			&coder->data->dongles[right].ts);
		if (has_burnt_out(coder))
			return (1);
	}
	// if (coder->id == 2 && coder->params.nb_compile == 1)
	// 	return (1);
	if (coder->data->failure)
		return (2);
	change_status(coder, DONGLE);
	return (0);
}

int	compile(t_coder *coder, int left, int right)
{
	int	failure;

	pthread_mutex_lock(&coder->data->dongles[left].mutex_dongle);
	pthread_mutex_lock(&coder->data->dongles[right].mutex_dongle);
	failure = wait(coder, left, right);
	if (failure == 1)
	{
		usleep(10000);
		change_status(coder, FAILURE);
		// coder->data->failure = 1;
	}
	if (coder->data->status.status[coder->data->status.index].state == FAILURE)
		return (unlock(coder, left, right));
	coder->data->dongles[left].to_who = coder->id;
	coder->data->dongles[right].to_who = coder->id;
	change_status(coder, COMPILING);
	add_time(&coder->spec, coder->params.burnout_time);
	coder->params.nb_compile++;
	usleep(coder->params.compile_time * 1000);
	unlock(coder, left, right);
	return (0);
}
