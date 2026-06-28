/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   steps.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/28 11:23:58 by maziza            #+#    #+#             */
/*   Updated: 2026/06/28 12:55:42 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int	compile(t_coder *coder, int left, int right)
{
	pthread_mutex_lock(&coder->data->dongles[left].mutex_dongle);
	while (!is_dongle_ready(coder->data->dongles[left], coder))
	{
		pthread_cond_wait(&coder->data->dongles[left].cond_dongle,
			&coder->data->dongles[left].mutex_dongle);
	}
	pthread_mutex_lock(&coder->data->dongles[right].mutex_dongle);
	while (!is_dongle_ready(coder->data->dongles[right], coder))
	{
		pthread_cond_wait(&coder->data->dongles[right].cond_dongle,
			&coder->data->dongles[right].mutex_dongle);
	}
	coder->params.nb_compile++;
	usleep(coder->params.compile_time * 1000);
	pthread_cond_signal(&coder->data->dongles[left].cond_dongle);
	pthread_cond_signal(&coder->data->dongles[right].cond_dongle);
	pthread_mutex_unlock(&coder->data->dongles[left].mutex_dongle);
	pthread_mutex_unlock(&coder->data->dongles[right].mutex_dongle);
	usleep(500000);
	return (1);
}

// void	*debug(t_coder *coder, int left, int right)
// {
// 	return (0);
// }

// void	*refactor(t_coder *coder, int left, int right)
// {
// 	return (0);
// }

int	execute_function(int function(t_coder *, int, int),
						t_coder *coder, int left, int right)
{
	int	result;

	result = function(coder, left, right);
	if (result == -1)
		return (1);
	if (result == 1)
		printf("Nb of compiles for Thread %d: %d\n", coder->id,
			coder->params.nb_compile);
	return (0);
}