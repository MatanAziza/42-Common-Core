/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/11 16:44:23 by maziza            #+#    #+#             */
/*   Updated: 2026/06/30 19:35:43 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <bits/pthreadtypes.h>
#include <pthread.h>
#include <unistd.h>

void	create_threads(pthread_t **p_threads, t_data *data)
{
	pthread_t	*threads;
	int			i;

	threads = *p_threads;
	i = 0;
	data->start = 0;
	while (i < data->params.nb_threads)
	{
		pthread_create(&threads[i], NULL, thread_function, &data->coders[i]);
		i++;
	}
	usleep(1000000);
	start_time(data);
}

int	end_threads(pthread_t **p_threads, t_data *data)
{
	pthread_t	*threads;
	int			i;

	threads = *p_threads;
	i = 0;
	while (i < data->params.nb_threads)
		pthread_join(threads[i++], NULL);
	free_all(p_threads, data);
	return (1);
}

int	values_check(t_data *data)
{
	printf("%p\n", data);
	return (0);
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
	if (values_check(&data))
		return (free_all(&threads, &data));
	data.failure = 0;
	create_threads(&threads, &data);
	end_threads(&threads, &data);
	if (!data.failure)
		printf("%sSuccess: All threads compiled%s\n", GREEN, WHITE);
	return (0);
}
