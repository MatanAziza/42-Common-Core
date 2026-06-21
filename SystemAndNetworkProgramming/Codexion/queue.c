/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   queue.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: matan </var/spool/mail/matan>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/21 11:39:31 by matan             #+#    #+#             */
/*   Updated: 2026/06/21 11:47:33 by matan            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"

void	add_r_queue(t_queue *queue, t_coder coder)
{
	while (queue != NULL)
}

void	add_to_queues(struct s_coder coder)
{
	t_queue *queues;
	t_queue queue_l;
	t_queue queue_r;
	int		left;
	int		right;

	queues = coder.queues;
	left = (coder.id + coder.nb_threads - 1) % coder.nb_threads;
	right = coder.id;
	queue_l = queues[left];
	queue_r = queues[right];

}
