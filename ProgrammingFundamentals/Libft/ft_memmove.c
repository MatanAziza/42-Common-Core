/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <maziza@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 11:13:08 by maziza            #+#    #+#             */
/*   Updated: 2025/11/13 09:33:32 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memmove(void *dest, const void *src, size_t n)
{
	unsigned char	*src1;
	unsigned char	*dest1;

	src1 = (unsigned char *)src;
	dest1 = (unsigned char *)dest;
	if (dest1 > src1 && dest1 < (src1 + n))
	{
		while (n--)
			dest1[n] = src1[n];
	}
	else
		ft_memcpy(dest, src, n);
	return (dest);
}
