/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 13:35:14 by maziza            #+#    #+#             */
/*   Updated: 2025/11/12 13:35:18 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../ft_printf.h"

int	ft_putnbr_base(long int nb, const char *base, int sign)
{
	char		c;
	long int	nbr;
	int			len;
	int			count;

	count = 0;
	if (sign == 0)
		nbr = (unsigned)nb;
	else
		nbr = nb;
	if (nbr < 0)
	{
		nbr = -nbr;
		count += ft_putchar('-');
		count += ft_putnbr_base(nbr, base, sign);
		return (count);
	}
	len = ft_strlen((char *)base);
	if (nbr / len != 0)
		count += ft_putnbr_base(nbr / len, base, sign);
	c = base[nbr % len];
	count += ft_putchar(c);
	return (count);
}
