/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_address.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 13:32:51 by maziza            #+#    #+#             */
/*   Updated: 2025/11/12 13:35:05 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../ft_printf.h"

int	ft_putnbr_address(unsigned long nbr, const char *base)
{
	char	c;
	int		count;

	count = 0;
	if (nbr / 16 != 0)
		count += ft_putnbr_address(nbr / 16, base);
	c = base[nbr % 16];
	count += ft_putchar(c);
	return (count);
}

int	ft_print_address(unsigned long address, const char *base)
{
	int	count;

	count = 0;
	if (address == 0)
		return (count + write(1, "(nil)", 5));
	count += write(1, "0x", 2);
	return (count + ft_putnbr_address(address, base));
}
