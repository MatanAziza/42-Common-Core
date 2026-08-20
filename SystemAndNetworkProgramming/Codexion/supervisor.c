/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   supervisor.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/03 10:56:33 by maziza            #+#    #+#             */
/*   Updated: 2026/08/14 14:46:46 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "colors.h"
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
	if (state == FAILURE)
		printf("%s%ld %d burnt out !\n", RED, status->status[index].timestamp, id);
	if (state == DONGLE)
	{
		printf("%s%ld %d got dongles\n", ORANGE,
			status->status[index].timestamp, id);
		printf("%s%ld %d got dongles\n", ORANGE,
			status->status[index].timestamp, id);
	}
	else if (state == COMPILING)
		printf("%s%ld %d is compiling\n", YELLOW,
			status->status[index].timestamp, id);
	else if (state == DEBUGGING)
		printf("%s%ld %d is debugging\n", BLUE,
			status->status[index].timestamp, id);
	else if (state == REFACTORING)
		printf("%s%ld %d is refactoring\n", VIOLET,
			status->status[index].timestamp, id);
}

void	change_status(t_coder *coder, enum e_CoderState state)
{
	t_status	*status;

	status = &coder->data->status;
	pthread_mutex_lock(&status->mutex_status);
	update_time(coder, state);
	status->status[status->index].timestamp = get_time_up(coder, coder->time);
	status->status[status->index].id = coder->id;
	status->status[status->index].state = state;
	if (state != FAILURE)
		status->index++;
	if (state == REFACTORING
		&& coder->params.nb_compile == coder->params.max_compile)
		status->status[status->index++].state = SUCCESS;
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
	while (status->index < status->length && !data->failure)
	{
		while (status->status[index].state == INIT)
			pthread_cond_wait(&status->cond_status, &status->mutex_status);
		print_status(status, index);
		index++;
	}
	pthread_mutex_unlock(&status->mutex_status);
	return (NULL);
}
