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
	t_dongle *dongle;

	dongle = &coder->data->dongles[dongle_id];
	if (coder->id == dongle_id)
	{
		dongle->right.id = coder->id;
		dongle->right.burnout = coder->spec;
		dongle->right.tv = coder->time;
	}
	else
	{
		dongle->left.id = coder->id;
		dongle->left.burnout = coder->spec;
		dongle->left.tv = coder->time;
	}
}

int		next_coder(t_coder *coder, t_dongle *dongle)
{
	if (dongle->right.id == -1)
		dongle->to_who = dongle->left.id;
	else if (dongle->left.id == -1)
		dongle->to_who = dongle->right.id;
	else
	{
		if (!strcmp(coder->params.mode, "fifo"))
			dongle->to_who = fifo(dongle);
		else if (!strcmp(coder->params.mode, "edf"))
			dongle->to_who = edf(dongle);
	}
	return (0);
}

void	update_dongle_queue(t_coder *coder, int left, int right)
{
	// Changer ses infos dans les 2 dongles
	update_queue_infos(coder, left);
	update_queue_infos(coder, right);
	// appeler fonction 2 fois qui renvoie a chaque dongle
	// l'id du to_who (selon fifo ou edf)
	next_coder(coder, &coder->data->dongles[left]);
	next_coder(coder, &coder->data->dongles[right]);
	return;
}
