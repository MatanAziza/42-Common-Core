/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <maziza@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 11:13:02 by maziza            #+#    #+#             */
/*   Updated: 2025/11/12 11:13:03 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memcpy(void *dest, const void *src, size_t n)
{
	size_t			i;
	unsigned char	*src1;
	unsigned char	*dest1;

	i = 0;
	src1 = (unsigned char *)src;
	dest1 = (unsigned char *)dest;
	while (i < n)
	{
		*dest1 = *src1;
		dest1++;
		src1++;
		i++;
	}
	return (dest);
}
