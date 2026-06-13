/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/11 16:44:23 by maziza            #+#    #+#             */
/*   Updated: 2026/06/12 18:30:03 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

void	*print_name(void *arg){
	int	*number;

	number = (int *)arg;
	printf("I'm a process and my ID is %d\n", *number);
	return NULL;
}

int	main(int argc, char **argv){
	int			nb_thread;
	pthread_t	*threads;
	int			*ids;
	int			i;

	nb_thread = atoi(argv[argc - 1]);
	printf("Nb threads: %d\n", nb_thread);
	threads = malloc(sizeof(pthread_t) * nb_thread);
	ids = malloc(sizeof(int) * (nb_thread + 1));
	i = 0;
	while (i < nb_thread){
		ids[i] = i;
		pthread_create(&threads[i], NULL, print_name, (void *)&ids[i]);
		i++;
	}
	i = 0;
	usleep(1000000);
	while (i < nb_thread)
		pthread_join(threads[i++], NULL);
	return (0);
}
