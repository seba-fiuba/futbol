<script>
	import { onMount } from 'svelte';
	import { fetchEquipos, fetchPartidos } from '$lib/api';

	let equipos = [];
	let partidos = [];
	let loading = true;
	let error = null;

	onMount(async () => {
		try {
			[equipos, partidos] = await Promise.all([fetchEquipos(), fetchPartidos()]);
		} catch (e) {
			error = e.message;
		} finally {
			loading = false;
		}
	});

	function getEquipoStats(equipoId) {
		let victorias = 0;
		let empates = 0;
		let derrotas = 0;
		let golesFavor = 0;
		let golesContra = 0;

		partidos.forEach((p) => {
			if (p.equipo_local_id === equipoId) {
				golesFavor += p.goles_local;
				golesContra += p.goles_visitante;
				if (p.goles_local > p.goles_visitante) victorias++;
				else if (p.goles_local === p.goles_visitante) empates++;
				else derrotas++;
			} else if (p.equipo_visitante_id === equipoId) {
				golesFavor += p.goles_visitante;
				golesContra += p.goles_local;
				if (p.goles_visitante > p.goles_local) victorias++;
				else if (p.goles_visitante === p.goles_local) empates++;
				else derrotas++;
			}
		});

		const puntos = victorias * 3 + empates;
		const partidosJugados = victorias + empates + derrotas;

		return { victorias, empates, derrotas, golesFavor, golesContra, puntos, partidosJugados };
	}

	$: equiposConStats = equipos
		.map((e) => ({ ...e, ...getEquipoStats(e.id) }))
		.sort((a, b) => b.puntos - a.puntos || b.golesFavor - b.golesContra - (a.golesFavor - a.golesContra));
</script>

<svelte:head>
	<title>Equipos - Fútbol Manager</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<h1 class="text-2xl md:text-3xl font-bold text-gray-800">🏆 Equipos y Tabla de Posiciones</h1>
	</div>

	{#if loading}
		<div class="text-center py-12">
			<div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
			<p class="mt-4 text-gray-600">Cargando equipos...</p>
		</div>
	{:else if error}
		<div class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
			<p class="font-semibold">Error:</p>
			<p>{error}</p>
		</div>
	{:else if equipos.length === 0}
		<div class="bg-gray-50 rounded-lg p-12 text-center">
			<p class="text-gray-600 text-lg">No hay equipos registrados</p>
		</div>
	{:else}
		<div class="bg-white rounded-lg shadow-md overflow-hidden">
			<!-- Tablet/Desktop: Tabla completa -->
			<div class="hidden md:block overflow-x-auto">
				<table class="w-full">
					<thead class="bg-green-600 text-white">
						<tr>
							<th class="px-4 py-3 text-left text-sm font-semibold">Pos</th>
							<th class="px-4 py-3 text-left text-sm font-semibold">Equipo</th>
							<th class="px-4 py-3 text-center text-sm font-semibold">PJ</th>
							<th class="px-4 py-3 text-center text-sm font-semibold">PG</th>
							<th class="px-4 py-3 text-center text-sm font-semibold">PE</th>
							<th class="px-4 py-3 text-center text-sm font-semibold">PP</th>
							<th class="px-4 py-3 text-center text-sm font-semibold">GF</th>
							<th class="px-4 py-3 text-center text-sm font-semibold">GC</th>
							<th class="px-4 py-3 text-center text-sm font-semibold">DIF</th>
							<th class="px-4 py-3 text-center text-sm font-semibold">PTS</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-200">
						{#each equiposConStats as equipo, i}
							<tr class="hover:bg-gray-50 transition-colors">
								<td class="px-4 py-3 text-sm font-bold text-gray-700">{i + 1}</td>
								<td class="px-4 py-3">
									<div class="flex items-center space-x-2">
										<span class="text-2xl">⚽</span>
										<span class="font-semibold text-gray-800">{equipo.nombre}</span>
									</div>
								</td>
								<td class="px-4 py-3 text-center text-sm text-gray-700">{equipo.partidosJugados}</td>
								<td class="px-4 py-3 text-center text-sm text-green-600 font-semibold">{equipo.victorias}</td>
								<td class="px-4 py-3 text-center text-sm text-gray-600">{equipo.empates}</td>
								<td class="px-4 py-3 text-center text-sm text-red-600 font-semibold">{equipo.derrotas}</td>
								<td class="px-4 py-3 text-center text-sm text-gray-700">{equipo.golesFavor}</td>
								<td class="px-4 py-3 text-center text-sm text-gray-700">{equipo.golesContra}</td>
								<td class="px-4 py-3 text-center text-sm font-semibold {equipo.golesFavor - equipo.golesContra > 0 ? 'text-green-600' : equipo.golesFavor - equipo.golesContra < 0 ? 'text-red-600' : 'text-gray-600'}">
									{equipo.golesFavor - equipo.golesContra > 0 ? '+' : ''}{equipo.golesFavor - equipo.golesContra}
								</td>
								<td class="px-4 py-3 text-center text-lg font-bold text-green-600">{equipo.puntos}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			<!-- Mobile: Vista de tarjetas mejorada -->
			<div class="md:hidden space-y-4 p-4">
				{#each equiposConStats as equipo, i}
					<div class="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-5 border-2 border-green-200 shadow-sm">
						<!-- Header de tarjeta -->
						<div class="flex items-center justify-between mb-4 pb-3 border-b-2 border-green-200">
							<div class="flex items-center space-x-3">
								<div class="bg-green-600 text-white w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg">
									{i + 1}
								</div>
								<div>
									<h3 class="font-bold text-gray-800 text-lg">{equipo.nombre}</h3>
									<span class="text-xs text-gray-600">{equipo.partidosJugados} partidos jugados</span>
								</div>
							</div>
							<div class="text-right">
								<div class="text-3xl font-bold text-green-600">{equipo.puntos}</div>
								<div class="text-xs text-gray-600 font-semibold">Puntos</div>
							</div>
						</div>

						<!-- Estadísticas en 2 filas -->
						<div class="space-y-3">
							<!-- Fila 1: Resultados -->
							<div class="grid grid-cols-3 gap-3">
								<div class="bg-white rounded-lg p-3 text-center border-l-4 border-green-500">
									<div class="text-2xl font-bold text-green-600">{equipo.victorias}</div>
									<div class="text-xs text-gray-600 font-semibold">Ganados</div>
								</div>
								<div class="bg-white rounded-lg p-3 text-center border-l-4 border-yellow-500">
									<div class="text-2xl font-bold text-yellow-600">{equipo.empates}</div>
									<div class="text-xs text-gray-600 font-semibold">Empatados</div>
								</div>
								<div class="bg-white rounded-lg p-3 text-center border-l-4 border-red-500">
									<div class="text-2xl font-bold text-red-600">{equipo.derrotas}</div>
									<div class="text-xs text-gray-600 font-semibold">Perdidos</div>
								</div>
							</div>

							<!-- Fila 2: Goles -->
							<div class="grid grid-cols-3 gap-3">
								<div class="bg-white rounded-lg p-3 text-center">
									<div class="text-sm text-gray-600 font-semibold">GF</div>
									<div class="text-2xl font-bold text-gray-800">{equipo.golesFavor}</div>
								</div>
								<div class="bg-white rounded-lg p-3 text-center">
									<div class="text-sm text-gray-600 font-semibold">GC</div>
									<div class="text-2xl font-bold text-gray-800">{equipo.golesContra}</div>
								</div>
								<div class="bg-white rounded-lg p-3 text-center">
									<div class="text-sm text-gray-600 font-semibold">DIF</div>
									<div class="text-2xl font-bold {equipo.golesFavor - equipo.golesContra > 0 ? 'text-green-600' : equipo.golesFavor - equipo.golesContra < 0 ? 'text-red-600' : 'text-gray-600'}">
										{equipo.golesFavor - equipo.golesContra > 0 ? '+' : ''}{equipo.golesFavor - equipo.golesContra}
									</div>
								</div>
							</div>
						</div>
					</div>
				{/each}
			</div>
		</div>

		<!-- Legend -->
		<div class="bg-white rounded-lg shadow-md p-4">
			<h3 class="font-semibold text-gray-800 mb-2">Leyenda:</h3>
			<div class="grid grid-cols-2 md:grid-cols-5 gap-2 text-sm text-gray-600">
				<div><span class="font-semibold">PJ:</span> Partidos Jugados</div>
				<div><span class="font-semibold">PG:</span> Partidos Ganados</div>
				<div><span class="font-semibold">PE:</span> Partidos Empatados</div>
				<div><span class="font-semibold">PP:</span> Partidos Perdidos</div>
				<div><span class="font-semibold">GF:</span> Goles a Favor</div>
				<div><span class="font-semibold">GC:</span> Goles en Contra</div>
				<div><span class="font-semibold">DIF:</span> Diferencia de Goles</div>
				<div><span class="font-semibold">PTS:</span> Puntos</div>
			</div>
		</div>
	{/if}
</div>
