/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   queue.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 16:34:47 by maziza            #+#    #+#             */
/*   Updated: 2026/06/25 13:50:11 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include <string.h>

void	update_queue_infos(t_coder *coder, int dongle_id)
{
	t_dongle	*dongle;
	int			index;

	dongle = &coder->data->dongles[dongle_id];
	index = dongle->queue_index;
	if (index > 1)
		index = 1;
	dongle->queue[index].id = coder->id;
	// printf("%d\n", dongle->queue[dongle->queue_index].id);
	dongle->queue[index].ts = coder->spec;
	dongle->queue[index].tv = coder->time;
	dongle->queue_index = index + 1;
}

void	fifo(t_dongle *dongle)
{
	dongle->to_who = dongle->queue[0].id;
	// printf("\033[0;37m%d, %d, %d\n", dongle->queue[0].id, dongle->queue[1].id, dongle->to_who);
	dongle->queue[0] = dongle->queue[1];
}

void	edf(t_dongle *dongle)
{
	if (dongle->queue[0].ts.tv_sec > dongle->queue[1].ts.tv_sec)
		dongle->to_who = dongle->queue[1].id;
	else if (dongle->queue[0].ts.tv_sec < dongle->queue[1].ts.tv_sec)
		dongle->to_who = dongle->queue[0].id;
	else
	{
		if (dongle->queue[0].ts.tv_nsec > dongle->queue[1].ts.tv_nsec)
			dongle->to_who = dongle->queue[1].id;
		else if (dongle->queue[0].ts.tv_nsec < dongle->queue[1].ts.tv_nsec)
			dongle->to_who = dongle->queue[0].id;
		else
			dongle->to_who = -1;
	}
	dongle->queue[0] = dongle->queue[1];
	// printf("edf\n");
}

int	next_coder(t_coder *coder, t_dongle *dongle)
{
	if (dongle->queue_index == 1)
		dongle->to_who = dongle->queue[0].id ;
	else
	{
		if (!strcmp(coder->params.mode, "fifo"))
			fifo(dongle);
		else if (!strcmp(coder->params.mode, "edf"))
			edf(dongle);
		else
			dongle->to_who = -1;
	}
	// printf("Dongle %d owned by %d\n", dongle->queue[0].id, dongle->to_who);
	return (0);
}

void	update_dongle_queue(t_coder *coder, int left, int right)
{
	pthread_mutex_lock(&coder->data->dongles[left].mutex_dongle);
	clock_gettime(0, &coder->data->dongles[left].ts);
	coder->data->dongles[left].last_ts = coder->data->dongles[left].ts;
	update_queue_infos(coder, left);
	next_coder(coder, &coder->data->dongles[left]);
	pthread_mutex_unlock(&coder->data->dongles[left].mutex_dongle);
	pthread_mutex_lock(&coder->data->dongles[right].mutex_dongle);
	clock_gettime(0, &coder->data->dongles[right].ts);
	coder->data->dongles[right].last_ts = coder->data->dongles[right].ts;
	update_queue_infos(coder, right);
	next_coder(coder, &coder->data->dongles[right]);
	pthread_mutex_unlock(&coder->data->dongles[right].mutex_dongle);
	return ;
}
