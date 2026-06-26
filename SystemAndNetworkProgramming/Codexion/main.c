/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/11 16:44:23 by maziza            #+#    #+#             */
/*   Updated: 2026/06/25 14:22:44 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <bits/pthreadtypes.h>
#include <unistd.h>

void	create_threads(pthread_t **p_threads, t_data *data)
{
	pthread_t	*threads;
	int			i;

	threads = *p_threads;
	i = 0;
	while (i < data->params.nb_threads)
	{
		pthread_create(&threads[i], NULL, thread_function, &data->coders[i]);
		i++;
	}
}

void	end_threads(pthread_t **p_threads, t_data data)
{
	pthread_t	*threads;
	int			i;

	threads = *p_threads;
	i = 0;
	while (i < data.params.nb_threads)
		pthread_join(threads[i++], NULL);
}

int	error_management(t_data data)
{
	int	i;
	int	count;

	return (0);
	while (1)
	{
		i = 0;
		count = 0;
		while (i < data.params.nb_threads)
		{
			if (data.states[i] == FAILURE)
				return (1);
			if (data.states[i] == SUCCESS)
				count++;
			i++;
		}
		if (count == i)
			return (0);
	}
}

int	main(int argc, char **argv)
{
	t_data		data;
	pthread_t	*threads;

	if (argc != 9)
		return (0 * printf("Wrong number of args.\n"));
	if (filler(argv, &data))
		return (1);
	threads = malloc(sizeof(pthread_t) * data.params.nb_threads);
	if (!threads)
		return (1);
	create_threads(&threads, &data);
	if (error_management(data))
		return (free_all(&threads, &data));
	end_threads(&threads, data);
	free_all(&threads, &data);
	return (0);
}
