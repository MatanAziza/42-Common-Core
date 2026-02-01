/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <maziza@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 11:12:07 by maziza            #+#    #+#             */
/*   Updated: 2025/11/12 11:12:07 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_calloc(size_t nmemb, size_t size)
{
	void	*buffer;
	size_t	max_size;
	size_t	mallsize;

	max_size = (size_t)-1;
	if (size == 0 || nmemb == 0)
		return (malloc(1));
	if (size > max_size / nmemb)
		return (NULL);
	else
		mallsize = size * nmemb;
	buffer = malloc(mallsize);
	if (!buffer)
		return (NULL);
	ft_bzero(buffer, mallsize);
	return (buffer);
}
