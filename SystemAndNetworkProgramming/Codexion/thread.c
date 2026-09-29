/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   thread.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/25 13:45:14 by maziza            #+#    #+#             */
/*   Updated: 2026/08/14 14:59:51 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <errno.h>
#include <sys/time.h>
#include <time.h>

t_coder	fill_coder(t_data *data, int id)
{
	t_coder	coder;

	coder.id = id;
	coder.params = data->params;
	coder.data = data;
	return (coder);
}

int	is_dongle_ready(t_dongle *dongle, t_coder *coder)
{
	return (dongle->to_who == coder->id);
}

int	is_ts_same(t_dongle *dongle1, t_dongle *dongle2)
{
	int	is_ts_same1;
	int	is_ts_same2;

	is_ts_same1 = (dongle1->last_ts.tv_sec == dongle1->ts.tv_sec
			&& dongle1->last_ts.tv_nsec == dongle1->ts.tv_nsec);
	is_ts_same2 = (dongle2->last_ts.tv_sec == dongle2->ts.tv_sec
			&& dongle2->last_ts.tv_nsec == dongle2->ts.tv_nsec);
	if (!is_ts_same1)
	{
		dongle1->last_ts.tv_sec = dongle1->ts.tv_sec;
		dongle1->last_ts.tv_nsec = dongle1->ts.tv_nsec;
	}
	if (!is_ts_same2)
	{
		dongle2->last_ts.tv_sec = dongle2->ts.tv_sec;
		dongle2->last_ts.tv_nsec = dongle2->ts.tv_nsec;
	}
	return (is_ts_same1 && is_ts_same2);
}

int	execute_function(int function(t_coder *, int, int), t_coder *coder,
		int left, int right)
{
	int	result;

	result = function(coder, left, right);
	if (result || coder->data->failure)
		return (1);
	return (0);
}

void	*thread_function(void *arg)
{
	t_coder	*coder;
	int		left;
	int		right;

	coder = (t_coder *)arg;
	left = coder->id;
	right = (left + 1) % coder->params.nb_threads;
	swap(&right, &left, right < left);
	while (!coder->data->start)
		usleep(1);
	update_time(coder, COMPILING);
	update_dongle_queue(coder, left, right);
	add_time(&coder->spec, coder->params.burnout_time);
	while (coder->params.nb_compile < coder->params.max_compile)
	{
		if (execute_function(compile, coder, left, right))
			return (NULL);
		if (execute_function(debug, coder, left, right))
			return (NULL);
		if (execute_function(refactor, coder, left, right))
			return (NULL);
	}
	return (NULL);
}
