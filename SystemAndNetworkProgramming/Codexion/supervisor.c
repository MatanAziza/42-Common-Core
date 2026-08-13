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

void	change_status(long time, t_coder *coder, enum e_CoderState state)
{
	t_status	*status;

	status = &coder->data->status;
	pthread_mutex_lock(&status->mutex_status);
	status->status[status->index].timestamp = time;
	status->status[status->index].timestamp = coder->id;
	status->status[status->index].timestamp = state;
	status->index += 1;
	if (state == FAILURE)
		coder->data->failure = 1;
	if (state == REFACTORING
		&& coder->params.nb_compile == coder->params.max_compile){
		status->status[status->index].state = SUCCESS;
		status->index += 1;
	}
	printf("Coder %d, state %d, counter %d\n", coder->id, state,
		status->counter);
	pthread_mutex_unlock(&status->mutex_status);
}

void	print_status(t_status *status)
{
	enum e_CoderState	state;
	int					id;

	state = status->status[status->index].state;
	id = status->status[status->index].id;
	if (state == DONGLE)
		printf("%d got dongles\n", id);
	else if (state == COMPILING)
		printf("%d is compiling\n", id);
	else if (state == DEBUGGING)
		printf("%d is debugging\n", id);
	else if (state == REFACTORING)
		printf("%d is refactoring\n", id);
	status->index++;
}

void	*supervise(void *arg)
{
	t_status	*status;
	t_data		*data;

	data = (t_data *)arg;
	status = &data->status;
	while (status->index < status->length)
	{
		while (status->status[status->index].state == INIT)
			continue;
		print_status(status);
	}
	printf("the end\n");
	return (NULL);
}
