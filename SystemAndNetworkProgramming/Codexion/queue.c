/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   queue.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 16:34:47 by maziza            #+#    #+#             */
/*   Updated: 2026/06/22 17:32:11 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"

void	remove_from_queue(t_queue *queue, int coder_id)
{
	t_node *node;

	node = queue->head;
	if (node->thread_id != coder_id)
		node->next = NULL;
	else
		queue->head = node->next;
}

int		fifo(t_queue *queue)
{
	int	to_who;

	to_who = queue->head->thread_id;
	remove_from_queue(queue, to_who);
	return (to_who);
}

int		edf(t_queue *queue)
{
	int		to_who;
	t_node	*node;


	node = queue->head;
	if (node)
		to_who = node->thread_id;
	if (node->next){
		if (node->last_compile > node->next->last_compile)
			to_who = node->next->thread_id;
	}
	remove_from_queue(queue, to_who);
	return (to_who);
}

void	add_queue(t_queue *queue, t_coder *coder)
{
	t_node *node;

	node = queue->head;
	if (node)
		node = node->next;
	node->thread_id = coder->id;
	node->last_compile = coder->last_compile;
}

void	add_to_queues(t_coder *coder)
{
	t_queue *queues;
	t_queue queue_l;
	t_queue queue_r;
	int		left;
	int		right;

	queues = coder->queues;
	left = (coder->id + coder->nb_threads - 1) % coder->nb_threads;
	right = coder->id;
	queue_l = queues[left];
	queue_r = queues[right];
	add_queue(&queue_l, coder);
	add_queue(&queue_r, coder);
}
