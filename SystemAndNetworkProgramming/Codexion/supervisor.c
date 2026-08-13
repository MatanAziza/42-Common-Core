/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   supervisor.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/03 10:56:33 by maziza            #+#    #+#             */
/*   Updated: 2026/08/11 13:21:14 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <pthread.h>
#include <sys/time.h>

void	print_status(t_status *status, int index)
{
	enum e_CoderState	state;
	int					id;

	state = status->status[index].state;
	id = status->status[index].id;
	// printf("%d, %d\n", state, id);
	if (state == DONGLE)
		printf("\033[0;3%dm %ld %d got dongles\n", id, status->status[index].timestamp, id);
	else if (state == COMPILING)
		printf("\033[0;3%dm %ld %d is compiling\n", id, status->status[index].timestamp, id);
	else if (state == DEBUGGING)
		printf("\033[0;3%dm %ld %d is debugging\n", id, status->status[index].timestamp, id);
	else if (state == REFACTORING)
		printf("\033[0;3%dm %ld %d is refactoring\n", id, status->status[index].timestamp, id);
}

void	change_status(long time, t_coder *coder, enum e_CoderState state)
{
	t_status	*status;

	status = &coder->data->status;
	pthread_mutex_lock(&status->mutex_status);
	status->status[status->index].timestamp = time;
	status->status[status->index].id = coder->id;
	status->status[status->index].state = state;
	// print_status(status, status->index);
	status->index++;
	if (state == FAILURE)
		coder->data->failure = 1;
	if (state == REFACTORING
		&& coder->params.nb_compile == coder->params.max_compile)
		status->status[status->index++].state = SUCCESS;
	// printf("Coder %d, state %d, counter %d\n", coder->id, state,
	// status->index);
	pthread_cond_broadcast(&status->cond_status);
	pthread_mutex_unlock(&status->mutex_status);
}

void	*supervise(void *arg)
{
	t_status	*status;
	t_data		*data;
	int			index;

	data = (t_data *)arg;
	status = &data->status;
	index = 0;
	pthread_mutex_lock(&status->mutex_status);
	while (status->index < status->length)
	{
		while (status->status[index].state == INIT)
			// printf("%d, ", status->status[index].state);
			// continue;
			pthread_cond_wait(&status->cond_status, &status->mutex_status);
		// printf("%d\n", index);
		print_status(status, index);
		index++;
	}
	// printf("the end\n");
	pthread_mutex_unlock(&status->mutex_status);
	return (NULL);
}
