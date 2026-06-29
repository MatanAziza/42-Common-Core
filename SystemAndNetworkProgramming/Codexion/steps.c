/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   steps.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/28 11:23:58 by maziza            #+#    #+#             */
/*   Updated: 2026/06/28 12:55:42 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <asm-generic/errno.h>
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

int	compile(t_coder *coder, int left, int right)
{
	int ret;

	add_burnout(coder);
	pthread_mutex_lock(&coder->data->dongles[left].mutex_dongle);
	while (!is_dongle_ready(coder->data->dongles[left], coder))
	{
		ret = pthread_cond_timedwait(&coder->data->dongles[left].cond_dongle,
			&coder->data->dongles[left].mutex_dongle,
			&coder->spec);
		if (ret == ETIMEDOUT || coder->data->failure)
			return (unlock(coder, left, right));
	}
	pthread_mutex_lock(&coder->data->dongles[right].mutex_dongle);
	while (!is_dongle_ready(coder->data->dongles[right], coder))
	{
		ret = pthread_cond_timedwait(&coder->data->dongles[right].cond_dongle,
			&coder->data->dongles[right].mutex_dongle,
			&coder->spec);
		if (ret == ETIMEDOUT || coder->data->failure)
			return (unlock(coder, left, right));
	}
	coder->params.nb_compile++;
	usleep(coder->params.compile_time * 1000);
	update_time(coder);
	unlock(coder, left, right);
	// usleep(500000);
	return (1);
}

int	debug(t_coder *coder, int left, int right)
{
	usleep(coder->params.debug_time * 1000);
	left += right;
	if (coder->data->failure)
		return (-2);
	gettimeofday(&coder->time, NULL);
	return (2);
}

int	refactor(t_coder *coder, int left, int right)
{
	usleep(coder->params.refactor_time * 1000);
	left += right;
	if (coder->data->failure)
		return (-2);
	gettimeofday(&coder->time, NULL);
	return (3);
}

int	execute_function(int function(t_coder *, int, int),
						t_coder *coder, int left, int right)
{
	int	result;

	result = function(coder, left, right);
	if (result == -2)
		return (1);
	else if (result == -1){
		coder->data->failure = 1;
		return (1 + 0 * printf("ERROR in coder %d\n", coder->id));
	}
	else if (result == 1)
		printf("%ld : Thread %d compiled for the %d time\n",
		 	get_time_up(coder), coder->id, coder->params.nb_compile);
	else if (result == 2)
		printf("%ld : Thread %d debugged\n", get_time_up(coder),
		 	coder->id);
	else if (result == 3)
		printf("%ld : Thread %d refactored\n", get_time_up(coder),
		 	coder->id);
	return (0);
}
