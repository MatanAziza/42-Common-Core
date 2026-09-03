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
	int				is_ts_same;

	is_ts_same = (dongle->last_ts.tv_sec == dongle->ts.tv_sec && dongle->last_ts.tv_nsec == dongle->ts.tv_nsec);
	// printf("Coder %d for %d %d, ts_same = %d\n", coder->id, dongle->left.id, dongle->right.id, is_ts_same);
	if ((dongle->to_who == -1 || dongle->to_who == coder->id) && is_ts_same)
		return (1);
	dongle->last_ts.tv_sec = dongle->ts.tv_sec;
	dongle->last_ts.tv_nsec = dongle->ts.tv_nsec;
	return (0);
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
	// printf("%ld.%ld start adding\n", coder->spec.tv_sec % 100, coder->spec.tv_nsec / 1000000);
	add_time(&coder->spec, coder->params.burnout_time);
	// printf("%ld.%ld start adding 2\n", coder->spec.tv_sec % 100, coder->spec.tv_nsec / 1000000);
	clock_gettime(0, &coder->data->dongles[left].ts);
	clock_gettime(0, &coder->data->dongles[right].ts);
	coder->data->dongles[left].last_ts = coder->data->dongles[left].ts;
	coder->data->dongles[right].last_ts = coder->data->dongles[right].ts;
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
