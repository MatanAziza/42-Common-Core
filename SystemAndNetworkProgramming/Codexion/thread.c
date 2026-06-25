/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   thread.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/25 13:45:14 by maziza            #+#    #+#             */
/*   Updated: 2026/06/25 14:22:39 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"

t_coder	fill_coder(t_data *data, int id)
{
	t_coder	coder;

	coder.id = id;
	coder.state = WAITING;
	coder.params = data->params;
	coder.data = data;
	return (coder);
}

int	is_dongle_ready(t_dongle dongle, t_coder *coder)
{
	if (dongle.to_who == -1 || dongle.to_who == coder->id)
		return (1);
	return (0);
}

void	gather_resources(t_coder *coder, int left, int right)
{
	pthread_mutex_lock(&coder->data->dongles[left].mutex_dongle);
	while (!is_dongle_ready(coder->data->dongles[left], coder))
	{
		printf("ID: %d, L: %d, R: %d\n", coder->id, left, right);
		pthread_cond_wait(&coder->data->dongles[left].cond_dongle,
			&coder->data->dongles[left].mutex_dongle);
	}
	pthread_mutex_lock(&coder->data->dongles[right].mutex_dongle);
	while (!is_dongle_ready(coder->data->dongles[right], coder))
	{
		printf("ID2: %d, L: %d, R: %d\n", coder->id, left, right);
		pthread_cond_wait(&coder->data->dongles[right].cond_dongle,
			&coder->data->dongles[right].mutex_dongle);
	}
}

void	*print_name(void *arg)
{
	t_coder	*coder;

	coder = (t_coder *)arg;
	printf("I am coder n %d\n", coder->id);
	return (NULL);
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
	while (coder->params.nb_compile < coder->params.max_compile)
	{
		gather_resources(coder, left, right);
		coder->params.nb_compile++;
		printf("Nb of compiles for Thread %d: %d\n", coder->id,
			coder->params.nb_compile);
		usleep(500000);
		pthread_cond_signal(&coder->data->dongles[left].cond_dongle);
		pthread_cond_signal(&coder->data->dongles[right].cond_dongle);
		pthread_mutex_unlock(&coder->data->dongles[left].mutex_dongle);
		pthread_mutex_unlock(&coder->data->dongles[right].mutex_dongle);
		usleep(500000);
	}
	return (NULL);
}
