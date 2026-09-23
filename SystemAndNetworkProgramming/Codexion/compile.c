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
	pthread_mutex_lock(&coder->data->dongles[left].mutex_dongle);
	clock_gettime(0, &coder->data->dongles[left].ts);
	// printf("Before %d: %ld.%ld\n",coder->id, coder->data->dongles[left].ts.tv_sec, coder->data->dongles[left].ts.tv_nsec);
	add_time(&coder->data->dongles[left].ts, coder->params.dongle_cooldown);
	update_queue_infos(coder, left);
	next_coder(coder, &coder->data->dongles[left]);
	// printf("After %d: %ld.%ld\n", coder->id, coder->data->dongles[left].ts.tv_sec, coder->data->dongles[left].ts.tv_nsec);
	pthread_mutex_unlock(&coder->data->dongles[left].mutex_dongle);
	pthread_mutex_lock(&coder->data->dongles[right].mutex_dongle);
	clock_gettime(0, &coder->data->dongles[right].ts);
	add_time(&coder->data->dongles[right].ts, coder->params.dongle_cooldown);
	update_queue_infos(coder, right);
	next_coder(coder, &coder->data->dongles[right]);
	pthread_mutex_unlock(&coder->data->dongles[right].mutex_dongle);
	return (1);
}

int	has_burnt_out(t_coder *coder)
{
	struct timespec	ts;

	clock_gettime(0, &ts);
	if (coder->spec.tv_sec > ts.tv_sec)
		return (0);
	else if (coder->spec.tv_sec == ts.tv_sec)
	{
		if (coder->spec.tv_nsec > ts.tv_nsec)
			return (0);
		else
			return (1);
	}
	return (1);
}

int	wait(t_coder *coder, int left, int right)
{
	// while (pas pour moi)
	// 	check burnout
	// while (1)
	// 	custom_timedwait
	// 	is_ts_same
	// 	si (is_ts_same)
	// 		break
	// 	update_ts
	while (1)
	{
		if (is_dongle_ready(&coder->data->dongles[left], coder)
		    && is_dongle_ready(&coder->data->dongles[right], coder))
			break;
		if (has_burnt_out(coder))
			return (1);
	}
	// printf("%d left waiting zone\n", coder->id);
	while (1)
	{
		custom_timedwait(&coder->data->dongles[left].ts);
		custom_timedwait(&coder->data->dongles[right].ts);
		// printf("%d got there\n", coder->id);
		if (has_burnt_out(coder))
			return (1);
		if (is_ts_same(&coder->data->dongles[left], &coder->data->dongles[right]))
			break;
	}
	if (coder->data->failure)
		return (2);
	change_status(coder, DONGLE);
	return (0);
}

int	compile(t_coder *coder, int left, int right)
{
	int	failure;

	failure = wait(coder, left, right);
	if (failure == 1)
	{
		usleep(10000);
		change_status(coder, FAILURE);
	}
	if (coder->data->status.status[coder->data->status.index].state == FAILURE)
		return (1);
	// coder->data->dongles[left].to_who = coder->id;
	// coder->data->dongles[right].to_who = coder->id;
	change_status(coder, COMPILING);
	add_time(&coder->spec, coder->params.burnout_time);
	coder->params.nb_compile++;
	usleep(coder->params.compile_time * 1000);
	unlock(coder, left, right);
	// for (int i = 0;i < coder->params.nb_threads;i++){
	// 	printf("%d Dongle %d for %d\n",coder->id, i, coder->data->dongles[i].to_who);
	// }
	return (0);
}
