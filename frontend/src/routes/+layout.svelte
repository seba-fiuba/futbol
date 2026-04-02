<script>
	import '../app.css';
	import ToastContainer from '$lib/components/ToastContainer.svelte';
	import { page } from '$app/stores';

	const nav = [
		{ href: '/', label: 'Inicio', icon: '🏠' },
		{ href: '/jugadores', label: 'Jugadores', icon: '👥' },
		{ href: '/equipos', label: 'Equipos', icon: '🏆' },
		{ href: '/partidos', label: 'Partidos', icon: '⚽' },
		{ href: '/goleadores', label: 'Goleadores', icon: '🎯' }
	];

	let mobileMenuOpen = false;
</script>

<div class="min-h-screen flex flex-col">
	<!-- Navbar -->
	<nav class="bg-green-600 text-white shadow-lg">
		<div class="container mx-auto px-4">
			<div class="flex items-center justify-between h-16">
<a href="/" class="flex items-center space-x-2 hover:opacity-80 transition-opacity">
				<span class="text-2xl">⚽</span>
				<span class="text-lg md:text-xl font-bold">Fútbol Manager</span>
			</a>
				
				<!-- Desktop Menu -->
				<div class="hidden md:flex space-x-1">
					{#each nav as item}
						<a
							href={item.href}
							class="px-4 py-2 rounded-md transition-colors {$page.url.pathname === item.href
								? 'bg-green-700 font-semibold'
								: 'hover:bg-green-500'}"
						>
							{item.label}
						</a>
					{/each}
				</div>

				<!-- Mobile Menu Button -->
				<button
					on:click={() => (mobileMenuOpen = !mobileMenuOpen)}
					class="md:hidden p-2 rounded-md hover:bg-green-500 transition-colors"
					aria-label="Toggle menu"
				>
					<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						{#if mobileMenuOpen}
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
						{:else}
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
						{/if}
					</svg>
				</button>
			</div>

			<!-- Mobile Menu -->
			{#if mobileMenuOpen}
				<div class="md:hidden py-4 space-y-2">
					{#each nav as item}
						<a
							href={item.href}
							on:click={() => (mobileMenuOpen = false)}
							class="flex items-center space-x-3 px-4 py-3 rounded-md transition-colors {$page.url.pathname === item.href
								? 'bg-green-700 font-semibold'
								: 'hover:bg-green-500'}"
						>
							<span class="text-xl">{item.icon}</span>
							<span>{item.label}</span>
						</a>
					{/each}
				</div>
			{/if}
		</div>
	</nav>

	<!-- Main Content -->
	<main class="flex-1 container mx-auto px-4 py-8">
		<slot />
	</main>

	<!-- Footer -->
	<footer class="bg-gray-800 text-white py-4 mt-auto">
		<div class="container mx-auto px-4 text-center">
			<p>Fútbol Manager © 2026</p>
		</div>
	</footer>

	<ToastContainer />
</div>
