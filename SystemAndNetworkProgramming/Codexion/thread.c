/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   thread.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/25 13:45:14 by maziza            #+#    #+#             */
/*   Updated: 2026/08/03 11:47:29 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <errno.h>
#include <sys/time.h>

t_coder	fill_coder(t_data *data, int id)
{
	t_coder	coder;

	coder.id = id;
	coder.params = data->params;
	coder.data = data;
	return (coder);
}

int	is_dongle_ready(t_dongle dongle, t_coder *coder)
{
	if ((dongle.to_who == -1 || dongle.to_who == coder->id) && 1)
		return (1);
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
	update_time(coder, 4);
	while (coder->params.nb_compile < coder->params.max_compile)
	{
		if (execute_function(compile, coder, left, right))
			return (NULL);
		if (execute_function(debug, coder, left, right))
			return (NULL);
		if (execute_function(refactor, coder, left, right))
			return (NULL);
	}
	printf("%d the end\n", coder->id);
	return (NULL);
}
