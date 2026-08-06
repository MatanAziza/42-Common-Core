/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   supervisor.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/03 10:56:33 by maziza            #+#    #+#             */
/*   Updated: 2026/08/03 11:47:24 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <pthread.h>
#include <sys/time.h>

void	change_status(long time, t_coder *coder, enum e_CoderState state)
{
	t_status	status;

	status = coder->data->status;
	pthread_mutex_lock(&status.mutex_status);
	status.timestamp = time;
	status.id = coder->id;
	status.state = state;
	if (state == COMPILING)
		status.counter += 1;
	printf("%d, %d\n", coder->id, state);
	pthread_mutex_unlock(&status.mutex_status);
}

int	is_status_ready(t_status *status)
{
	if (status->id != status->last_id || status->state != status->last_state)
		return (1);
	return (0);
}

void	update_status(t_status *status)
{
	status->last_id = status->id;
	status->last_state = status->state;
}

void	print_status(t_status *status)
{
	printf("%d, %d\n", status->id, status->state);
}

void	*supervise(void *arg)
{
	t_status	*status;
	t_data		*data;

	data = (t_data *)arg;
	status = &data->status;
	pthread_mutex_lock(&status->mutex_status);
	while (status->counter / data->params.nb_threads != data->params.max_compile)
	{
		while (!is_status_ready(status))
			pthread_cond_wait(&status->cond_status, &status->mutex_status);
		if (status->state == FAILURE){
			printf("hehe\n");
			data->failure = 1;
		}
		print_status(status);
		update_status(status);
	}
	pthread_mutex_unlock(&status->mutex_status);
	return (NULL);
}
