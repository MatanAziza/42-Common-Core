/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   free_mallocs.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/12 17:33:03 by maziza            #+#    #+#             */
/*   Updated: 2026/06/12 17:39:32 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int	free_values(int *values)
{
	free(values);
	return (1);
}

int	free_dongles(t_data *data)
{
	free(data->dongles);
	return (1);
}

int	free_coders(t_data *data)
{
	free(data->coders);
	return (1);
}

int	free_all(pthread_t **threads, t_data *data)
{
	free(*threads);
	free(data->dongles);
	free(data->coders);
	free(data->status.status);
	return (1);
}
