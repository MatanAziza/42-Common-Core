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

int	wait(t_coder *coder, int left, int right)
{
	struct timespec ts;

	clock_gettime(0, &ts);
	clock_gettime(0, &ts);
	printf("\033[1;31m%d %ld.%ld is dongle wait\n",coder->id, ts.tv_sec % 10, ts.tv_nsec);
	while (1)
	{
	pthread_cond_timedwait(&coder->data->dongles[left].cond_dongle,
		&coder->data->dongles[left].mutex_dongle,
		&coder->data->dongles[left].ts);
	pthread_cond_timedwait(&coder->data->dongles[right].cond_dongle,
		&coder->data->dongles[right].mutex_dongle,
		&coder->data->dongles[right].ts);
	if (is_dongle_ready(&coder->data->dongles[left], coder)
		&& is_dongle_ready(&coder->data->dongles[right], coder))
		break;
	}
	clock_gettime(0, &ts);
	printf("\033[1;31m%d %ld.%ld is end wait\n",coder->id, ts.tv_sec % 10, ts.tv_nsec);
	if (coder->data->failure)
		return (2);
	change_status(coder, DONGLE);
	add_time(&coder->spec, coder->params.burnout_time);
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
		// printf("%ld %d Start of BurnOut!\n", get_time_up(coder),coder->id);
		usleep(10000);
		change_status(coder, FAILURE);
		coder->data->failure = 1;
	}
	if (coder->data->status.status[coder->data->status.index].state == FAILURE)
		return (unlock(coder, left, right));
	coder->data->dongles[left].to_who = coder->id;
	coder->data->dongles[right].to_who = coder->id;
	// printf("%d to who = %d\n", coder->id, coder->data->dongles[left].to_who);
	// printf("%d to who = %d\n", coder->id, coder->data->dongles[right].to_who);
	change_status(coder, COMPILING);
	coder->params.nb_compile++;
	usleep(coder->params.compile_time * 1000);
	unlock(coder, left, right);
	return (0);
}
